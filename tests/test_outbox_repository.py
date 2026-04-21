from datetime import UTC, datetime, timedelta

import pytest

from shared.database.models import Checklist, Medication, NotificationOutbox, User
from shared.notifications import OutboxKind, OutboxRepository, OutboxStatus
from shared.notifications.outbox_repository import BACKOFF_SECONDS, MAX_ATTEMPTS

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def seeded(test_session):
    user = User(telegram_id=1, language="en")
    test_session.add(user)
    await test_session.flush()
    medication = Medication(
        user_id=user.id,
        name="Test Med",
        schedule="custom",
        time=datetime.now().time(),
    )
    test_session.add(medication)
    await test_session.flush()
    checklist = Checklist(
        user_id=user.id,
        medication_id=medication.id,
        date=datetime.now(UTC).date(),
        status=False,
    )
    test_session.add(checklist)
    await test_session.commit()
    return {"user": user, "medication": medication, "checklist": checklist}


async def _make_entry(
    repo: OutboxRepository,
    seeded: dict,
    *,
    due_at: datetime | None = None,
    kind: OutboxKind = OutboxKind.REMINDER,
) -> NotificationOutbox:
    return await repo.create(
        user_id=seeded["user"].id,
        medication_id=seeded["medication"].id,
        checklist_id=seeded["checklist"].id,
        kind=kind,
        due_at=due_at or datetime.now(UTC),
    )


async def test_create_inserts_pending_entry(test_session, seeded):
    repo = OutboxRepository(test_session)
    entry = await _make_entry(repo, seeded)
    assert entry.id is not None
    assert entry.status == str(OutboxStatus.PENDING)
    assert entry.attempts == 0
    assert entry.last_error is None


async def test_next_pending_returns_due_entry(test_session, seeded):
    repo = OutboxRepository(test_session)
    past = datetime.now(UTC) - timedelta(minutes=1)
    entry = await _make_entry(repo, seeded, due_at=past)
    await test_session.commit()

    found = await repo.next_pending()
    assert found is not None
    assert found.id == entry.id


async def test_next_pending_skips_future_entries(test_session, seeded):
    repo = OutboxRepository(test_session)
    future = datetime.now(UTC) + timedelta(hours=1)
    await _make_entry(repo, seeded, due_at=future)
    await test_session.commit()

    found = await repo.next_pending()
    assert found is None


async def test_mark_sent_updates_status(test_session, seeded):
    repo = OutboxRepository(test_session)
    entry = await _make_entry(repo, seeded)
    await test_session.commit()

    await repo.mark_sent(entry.id)
    await test_session.commit()

    refreshed = await repo.get(entry.id)
    assert refreshed.status == str(OutboxStatus.SENT)
    assert refreshed.last_error is None


async def test_mark_failed_backoff_and_retry(test_session, seeded):
    repo = OutboxRepository(test_session)
    entry = await _make_entry(repo, seeded, due_at=datetime.now(UTC))
    await test_session.commit()

    before = datetime.now(UTC)
    updated = await repo.mark_failed(entry.id, "network error")
    await test_session.commit()

    assert updated.attempts == 1
    assert updated.status == str(OutboxStatus.PENDING)
    assert updated.last_error == "network error"
    expected_delay = timedelta(seconds=BACKOFF_SECONDS[0])
    assert updated.due_at >= before + expected_delay - timedelta(seconds=2)


async def test_mark_failed_becomes_dead_after_max_attempts(test_session, seeded):
    repo = OutboxRepository(test_session)
    entry = await _make_entry(repo, seeded)
    entry.attempts = MAX_ATTEMPTS - 1
    await test_session.commit()

    updated = await repo.mark_failed(entry.id, "still broken")
    await test_session.commit()

    assert updated.attempts == MAX_ATTEMPTS
    assert updated.status == str(OutboxStatus.DEAD)


async def test_mark_dead_sets_status_and_error(test_session, seeded):
    repo = OutboxRepository(test_session)
    entry = await _make_entry(repo, seeded)
    await test_session.commit()

    await repo.mark_dead(entry.id, "permanent failure")
    await test_session.commit()

    refreshed = await repo.get(entry.id)
    assert refreshed.status == str(OutboxStatus.DEAD)
    assert refreshed.last_error == "permanent failure"


async def test_error_message_truncated(test_session, seeded):
    repo = OutboxRepository(test_session)
    entry = await _make_entry(repo, seeded)
    await test_session.commit()

    long_error = "x" * 5000
    await repo.mark_failed(entry.id, long_error)
    await test_session.commit()

    refreshed = await repo.get(entry.id)
    assert len(refreshed.last_error) == 2000
