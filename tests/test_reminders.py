from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from shared.database import db as shared_db
from shared.database.db import Base
from shared.database.models import Checklist, Medication, User, UserSettings


@pytest.fixture(autouse=True)
async def reminders_db(monkeypatch):
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    maker = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(shared_db, "engine", engine)
    monkeypatch.setattr(shared_db, "async_session_maker", maker)
    monkeypatch.setattr(shared_db, "_initialized", True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield maker
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
def bot():
    mock = MagicMock()
    mock.send_message = AsyncMock()
    mock.send_message.return_value = MagicMock(message_id=42)
    mock.delete_message = AsyncMock()
    return mock


@pytest.fixture
async def user_with_med(reminders_db):
    tz = ZoneInfo("Europe/Moscow")
    now = datetime.now(tz)
    past_time = (now - timedelta(minutes=30)).time().replace(microsecond=0)
    async with reminders_db() as session:
        user = User(telegram_id=111222333, language="ru", is_blocked=False)
        session.add(user)
        await session.flush()
        settings = UserSettings(
            user_id=user.id, reminders_enabled=True, reminder_repeat_minutes=30
        )
        session.add(settings)
        med = Medication(
            user_id=user.id,
            name="Test",
            schedule="custom",
            time=past_time,
        )
        session.add(med)
        await session.flush()
        checklist = Checklist(
            user_id=user.id,
            medication_id=med.id,
            date=now.date(),
            status=False,
        )
        session.add(checklist)
        await session.commit()
        return {
            "telegram_id": user.telegram_id,
            "user_id": user.id,
            "medication_id": med.id,
            "checklist_id": checklist.id,
        }


async def test_send_reminder_marks_reminder_sent_at(bot, user_with_med, reminders_db):
    from bot.services.reminders import send_medication_reminder

    await send_medication_reminder(bot, user_with_med["telegram_id"], user_with_med["medication_id"])

    bot.send_message.assert_awaited_once()
    async with reminders_db() as session:
        cl = await session.get(Checklist, user_with_med["checklist_id"])
        assert cl.reminder_sent_at is not None


async def test_send_reminder_skips_if_already_sent_today(bot, user_with_med, reminders_db):
    from bot.services.reminders import send_medication_reminder

    async with reminders_db() as session:
        cl = await session.get(Checklist, user_with_med["checklist_id"])
        cl.reminder_sent_at = datetime.now(UTC)
        await session.commit()

    await send_medication_reminder(bot, user_with_med["telegram_id"], user_with_med["medication_id"])

    bot.send_message.assert_not_awaited()


async def test_send_reminder_skips_if_already_taken(bot, user_with_med, reminders_db):
    from bot.services.reminders import send_medication_reminder

    async with reminders_db() as session:
        cl = await session.get(Checklist, user_with_med["checklist_id"])
        cl.status = True
        await session.commit()

    await send_medication_reminder(bot, user_with_med["telegram_id"], user_with_med["medication_id"])

    bot.send_message.assert_not_awaited()


async def test_catch_up_sends_past_due_unsent(bot, user_with_med):
    from bot.services.reminders import catch_up_missed_reminders

    await catch_up_missed_reminders(bot)

    bot.send_message.assert_awaited_once()


async def test_catch_up_skips_already_sent(bot, user_with_med, reminders_db):
    from bot.services.reminders import catch_up_missed_reminders

    async with reminders_db() as session:
        cl = await session.get(Checklist, user_with_med["checklist_id"])
        cl.reminder_sent_at = datetime.now(UTC)
        await session.commit()

    await catch_up_missed_reminders(bot)

    bot.send_message.assert_not_awaited()


async def test_catch_up_skips_already_taken(bot, user_with_med, reminders_db):
    from bot.services.reminders import catch_up_missed_reminders

    async with reminders_db() as session:
        cl = await session.get(Checklist, user_with_med["checklist_id"])
        cl.status = True
        await session.commit()

    await catch_up_missed_reminders(bot)

    bot.send_message.assert_not_awaited()


async def test_catch_up_skips_future_due(bot, reminders_db):
    from bot.services.reminders import catch_up_missed_reminders

    tz = ZoneInfo("Europe/Moscow")
    now = datetime.now(tz)
    future_time = (now + timedelta(hours=2)).time().replace(microsecond=0)

    async with reminders_db() as session:
        user = User(telegram_id=222333444, language="ru", is_blocked=False)
        session.add(user)
        await session.flush()
        settings = UserSettings(user_id=user.id, reminders_enabled=True, reminder_repeat_minutes=30)
        session.add(settings)
        med = Medication(user_id=user.id, name="Future", schedule="custom", time=future_time)
        session.add(med)
        await session.flush()
        checklist = Checklist(
            user_id=user.id,
            medication_id=med.id,
            date=now.date(),
            status=False,
        )
        session.add(checklist)
        await session.commit()

    await catch_up_missed_reminders(bot)

    bot.send_message.assert_not_awaited()


async def test_catch_up_skips_reminders_disabled(bot, user_with_med, reminders_db):
    from bot.services.reminders import catch_up_missed_reminders

    async with reminders_db() as session:
        from sqlalchemy import select as _select

        settings_row = (
            await session.execute(_select(UserSettings).where(UserSettings.user_id == user_with_med["user_id"]))
        ).scalar_one()
        settings_row.reminders_enabled = False
        await session.commit()

    await catch_up_missed_reminders(bot)

    bot.send_message.assert_not_awaited()


async def test_catch_up_skips_blocked_user(bot, user_with_med, reminders_db):
    from bot.services.reminders import catch_up_missed_reminders

    async with reminders_db() as session:
        user = await session.get(User, user_with_med["user_id"])
        user.is_blocked = True
        await session.commit()

    await catch_up_missed_reminders(bot)

    bot.send_message.assert_not_awaited()
