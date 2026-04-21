from datetime import UTC, datetime, timedelta
from enum import StrEnum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import NotificationOutbox

MAX_ATTEMPTS = 5
BACKOFF_SECONDS = (30, 60, 120, 300, 600)


class OutboxKind(StrEnum):
    REMINDER = "reminder"
    FOLLOWUP = "followup"


class OutboxStatus(StrEnum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DEAD = "dead"


def _backoff_delay(attempts: int) -> timedelta:
    idx = min(attempts - 1, len(BACKOFF_SECONDS) - 1)
    return timedelta(seconds=BACKOFF_SECONDS[idx])


class OutboxRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: int,
        medication_id: int,
        checklist_id: int,
        kind: OutboxKind,
        due_at: datetime,
    ) -> NotificationOutbox:
        entry = NotificationOutbox(
            user_id=user_id,
            medication_id=medication_id,
            checklist_id=checklist_id,
            kind=str(kind),
            due_at=due_at,
            status=str(OutboxStatus.PENDING),
            attempts=0,
        )
        self._session.add(entry)
        await self._session.flush()
        return entry

    async def get(self, outbox_id: int) -> NotificationOutbox | None:
        return await self._session.get(NotificationOutbox, outbox_id)

    async def next_pending(self, *, now: datetime | None = None) -> NotificationOutbox | None:
        now = now or datetime.now(UTC)
        query = (
            select(NotificationOutbox)
            .where(
                NotificationOutbox.status == str(OutboxStatus.PENDING),
                NotificationOutbox.due_at <= now,
            )
            .order_by(NotificationOutbox.due_at.asc())
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def mark_sent(self, outbox_id: int) -> None:
        entry = await self.get(outbox_id)
        if entry is None:
            return
        entry.status = str(OutboxStatus.SENT)
        entry.last_error = None
        await self._session.flush()

    async def mark_failed(self, outbox_id: int, error: str) -> NotificationOutbox | None:
        entry = await self.get(outbox_id)
        if entry is None:
            return None
        entry.attempts += 1
        entry.last_error = error[:2000]
        if entry.attempts >= MAX_ATTEMPTS:
            entry.status = str(OutboxStatus.DEAD)
        else:
            entry.status = str(OutboxStatus.PENDING)
            entry.due_at = datetime.now(UTC) + _backoff_delay(entry.attempts)
        await self._session.flush()
        return entry

    async def mark_dead(self, outbox_id: int, error: str) -> None:
        entry = await self.get(outbox_id)
        if entry is None:
            return
        entry.status = str(OutboxStatus.DEAD)
        entry.last_error = error[:2000]
        await self._session.flush()
