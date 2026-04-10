from datetime import date

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import Checklist, Medication


class ChecklistRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_user_and_date(
        self, user_id: int, target_date: date
    ) -> list[tuple[Checklist, Medication]]:
        query = (
            select(Checklist, Medication)
            .join(Medication, Checklist.medication_id == Medication.id)
            .where(Checklist.user_id == user_id, Checklist.date == target_date)
            .order_by(Medication.time)
        )
        result = await self._session.execute(query)
        return list(result.all())

    async def find_by_id_and_user(self, checklist_id: int, user_id: int) -> Checklist | None:
        query = select(Checklist).where(
            Checklist.id == checklist_id,
            Checklist.user_id == user_id,
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def update_status(self, checklist_id: int, user_id: int, status: bool) -> None:
        await self._session.execute(
            update(Checklist)
            .where(Checklist.id == checklist_id, Checklist.user_id == user_id)
            .values(status=status)
        )
        await self._session.flush()

    async def ensure_daily_checklist(
        self, user_id: int, medications: list[Medication], target_date: date
    ) -> None:
        existing_query = select(Checklist.medication_id).where(
            Checklist.user_id == user_id,
            Checklist.date == target_date,
        )
        existing_ids = set((await self._session.execute(existing_query)).scalars().all())
        missing = [m for m in medications if m.id not in existing_ids]
        for m in missing:
            self._session.add(
                Checklist(
                    user_id=user_id,
                    medication_id=m.id,
                    date=target_date,
                    status=False,
                )
            )
        if missing:
            await self._session.flush()
