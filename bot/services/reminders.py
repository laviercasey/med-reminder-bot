import logging
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from sqlalchemy import select

from bot.keyboards import get_reminder_action_keyboard
from bot.localization import get_text
from shared.config import settings
from shared.database.db import get_session
from shared.database.models import Checklist, Medication, User, UserSettings

DEFAULT_TZ = ZoneInfo("Europe/Moscow")
scheduler = AsyncIOScheduler()
logger = logging.getLogger("med_reminder_bot")


def _get_user_tz(user_settings: UserSettings | None) -> ZoneInfo:
    if user_settings and user_settings.timezone:
        try:
            return ZoneInfo(user_settings.timezone)
        except (KeyError, ValueError):
            return DEFAULT_TZ
    return DEFAULT_TZ


def _trigger_matches(trigger: CronTrigger, hour: int, minute: int, tz: ZoneInfo) -> bool:
    try:
        fields = {f.name: str(f) for f in trigger.fields}
        return (
            fields.get("hour") == str(hour)
            and fields.get("minute") == str(minute)
            and str(trigger.timezone) == str(tz)
        )
    except AttributeError:
        return False


_last_reminder_messages: dict[tuple[int, int], int] = {}


def _save_reminder_message(telegram_id: int, medication_id: int, message_id: int) -> None:
    _last_reminder_messages[(telegram_id, medication_id)] = message_id


async def _delete_previous_reminder(bot: Bot, telegram_id: int, medication_id: int) -> None:
    key = (telegram_id, medication_id)
    prev_msg_id = _last_reminder_messages.pop(key, None)
    if prev_msg_id is None:
        return
    try:
        await bot.delete_message(chat_id=telegram_id, message_id=prev_msg_id)
    except Exception:
        pass


def _today(tz: ZoneInfo | None = None) -> datetime.date:
    return datetime.now(tz or DEFAULT_TZ).date()


async def setup_daily_reminders(bot: Bot) -> None:
    logger.info("Setting up daily reminder jobs")

    scheduler.remove_all_jobs()

    scheduler.add_job(
        generate_daily_checklists,
        CronTrigger(hour=0, minute=1, timezone=DEFAULT_TZ),
        args=[bot],
        id="generate_checklists",
        coalesce=True,
        misfire_grace_time=3600,
    )

    scheduler.add_job(
        setup_medication_reminders,
        CronTrigger(minute=0, timezone=DEFAULT_TZ),
        args=[bot],
        id="periodic_resync",
        coalesce=True,
        misfire_grace_time=600,
    )

    await setup_medication_reminders(bot)

    if not scheduler.running:
        scheduler.start()

    await catch_up_missed_reminders(bot)


async def setup_medication_reminders(bot: Bot) -> None:
    logger.info("Setting up medication reminders")

    async with get_session() as session:
        query = (
            select(User, Medication, UserSettings)
            .join(Medication, User.id == Medication.user_id)
            .outerjoin(UserSettings, User.id == UserSettings.user_id)
            .where(User.is_blocked.is_(False))
        )

        result = await session.execute(query)
        current_reminder_ids: set[str] = set()

        for user, medication, user_settings in result:
            hour = medication.time.hour
            minute = medication.time.minute
            tz = _get_user_tz(user_settings)

            job_id = f"reminder_{medication.id}"
            current_reminder_ids.add(job_id)

            expected_args = [bot, user.telegram_id, medication.id]
            existing = scheduler.get_job(job_id)
            if existing is not None and _trigger_matches(
                existing.trigger, hour, minute, tz
            ) and list(existing.args) == expected_args:
                continue

            scheduler.add_job(
                send_medication_reminder,
                CronTrigger(hour=hour, minute=minute, timezone=tz),
                args=expected_args,
                id=job_id,
                replace_existing=True,
                coalesce=True,
                misfire_grace_time=300,
            )

    for j in scheduler.get_jobs():
        if j.id.startswith("reminder_") and j.id not in current_reminder_ids:
            scheduler.remove_job(j.id)


async def generate_daily_checklists(bot: Bot) -> None:
    logger.info("Generating daily checklists")

    async with get_session() as session:
        query = (
            select(User, Medication, UserSettings)
            .join(Medication, User.id == Medication.user_id)
            .outerjoin(UserSettings, User.id == UserSettings.user_id)
            .where(User.is_blocked.is_(False))
        )

        result = await session.execute(query)
        user_data: dict[int, tuple[ZoneInfo, list[Medication]]] = {}

        for user, medication, user_settings in result:
            if user.id not in user_data:
                tz = _get_user_tz(user_settings)
                user_data[user.id] = (tz, [])
            user_data[user.id][1].append(medication)

        for user_id, (tz, medications) in user_data.items():
            today = _today(tz)
            for medication in medications:
                checklist_query = select(Checklist).where(
                    Checklist.user_id == user_id,
                    Checklist.medication_id == medication.id,
                    Checklist.date == today,
                )

                checklist_exists = await session.execute(checklist_query)
                if checklist_exists.first() is None:
                    new_checklist = Checklist(
                        user_id=user_id,
                        medication_id=medication.id,
                        date=today,
                        status=False,
                    )
                    session.add(new_checklist)

        await session.commit()


async def send_medication_reminder(bot: Bot, telegram_id: int, medication_id: int) -> None:
    try:
        async with get_session() as session:
            user_query = select(User).where(User.telegram_id == telegram_id)
            user = (await session.execute(user_query)).scalar_one_or_none()

            if not user or user.is_blocked:
                return

            settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
            user_settings = (await session.execute(settings_query)).scalar_one_or_none()

            if user_settings and not user_settings.reminders_enabled:
                return

            medication_query = select(Medication).where(Medication.id == medication_id)
            medication = (await session.execute(medication_query)).scalar_one_or_none()

            if not medication:
                return

            tz = _get_user_tz(user_settings)
            today = _today(tz)
            checklist_query = select(Checklist).where(
                Checklist.user_id == user.id,
                Checklist.medication_id == medication_id,
                Checklist.date == today,
            )

            checklist = (await session.execute(checklist_query)).scalar_one_or_none()

            if checklist and checklist.status:
                logger.info("Skipping reminder for med %s - already taken", medication.name)
                return

            if checklist and checklist.reminder_sent_at is not None:
                sent_today = checklist.reminder_sent_at.astimezone(tz).date() == today
                if sent_today:
                    logger.info(
                        "Skipping reminder for med %s - already sent today", medication.name
                    )
                    return

            if not checklist:
                checklist = Checklist(
                    user_id=user.id,
                    medication_id=medication_id,
                    date=today,
                    status=False,
                )
                session.add(checklist)
                await session.flush()

            reminder_text = get_text("reminder", user.language, name=medication.name)

            await _delete_previous_reminder(bot, telegram_id, medication_id)

            sent = await bot.send_message(
                chat_id=telegram_id,
                text=reminder_text,
                reply_markup=get_reminder_action_keyboard(checklist.id, user.language),
            )
            _save_reminder_message(telegram_id, medication_id, sent.message_id)
            checklist.reminder_sent_at = datetime.now(UTC)
            await session.commit()

            repeat_minutes = settings.REMINDER_RETRY_MINUTES
            if user_settings:
                repeat_minutes = user_settings.reminder_repeat_minutes

            followup_time = datetime.now(tz) + timedelta(minutes=repeat_minutes)
            followup_job_id = f"followup_{medication_id}_{int(followup_time.timestamp())}"

            scheduler.add_job(
                send_followup_reminder,
                DateTrigger(run_date=followup_time),
                args=[bot, telegram_id, medication_id],
                id=followup_job_id,
                replace_existing=True,
            )

            logger.info(
                "Sent reminder for %s, follow-up in %s min",
                medication.name,
                repeat_minutes,
            )

    except Exception as e:
        logger.error("Error sending reminder: %s", e, exc_info=e)


async def catch_up_missed_reminders(bot: Bot) -> None:
    logger.info("Running catch-up for missed reminders")

    async with get_session() as session:
        query = (
            select(User, Medication, Checklist, UserSettings)
            .join(Medication, User.id == Medication.user_id)
            .join(
                Checklist,
                (Checklist.medication_id == Medication.id) & (Checklist.user_id == User.id),
            )
            .outerjoin(UserSettings, User.id == UserSettings.user_id)
            .where(User.is_blocked.is_(False))
            .where(Checklist.status.is_(False))
            .where(Checklist.reminder_sent_at.is_(None))
        )
        rows = list((await session.execute(query)).all())

    sent_count = 0
    for user, medication, checklist, user_settings in rows:
        if user_settings and not user_settings.reminders_enabled:
            continue
        tz = _get_user_tz(user_settings)
        if checklist.date != _today(tz):
            continue
        due_dt = datetime.combine(checklist.date, medication.time, tz)
        if due_dt > datetime.now(tz):
            continue
        try:
            await send_medication_reminder(bot, user.telegram_id, medication.id)
            sent_count += 1
        except Exception as e:
            logger.error("Catch-up send failed for med %s: %s", medication.id, e, exc_info=e)

    logger.info("Catch-up finished, sent %d missed reminders", sent_count)


async def send_followup_reminder(bot: Bot, telegram_id: int, medication_id: int) -> None:
    try:
        async with get_session() as session:
            user_query = select(User).where(User.telegram_id == telegram_id)
            user = (await session.execute(user_query)).scalar_one_or_none()

            if not user or user.is_blocked:
                return

            settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
            user_settings = (await session.execute(settings_query)).scalar_one_or_none()

            if user_settings and not user_settings.reminders_enabled:
                return

            medication_query = select(Medication).where(Medication.id == medication_id)
            medication = (await session.execute(medication_query)).scalar_one_or_none()

            if not medication:
                return

            tz = _get_user_tz(user_settings)
            today = _today(tz)
            checklist_query = select(Checklist).where(
                Checklist.user_id == user.id,
                Checklist.medication_id == medication_id,
                Checklist.date == today,
            )

            checklist = (await session.execute(checklist_query)).scalar_one_or_none()

            if not checklist or checklist.status:
                logger.info(
                    "Skipping follow-up for med %s - already taken or no checklist",
                    medication.name,
                )
                return

            reminder_text = get_text("reminder_repeat", user.language, name=medication.name)

            await _delete_previous_reminder(bot, telegram_id, medication_id)

            sent = await bot.send_message(
                chat_id=telegram_id,
                text=reminder_text,
                reply_markup=get_reminder_action_keyboard(checklist.id, user.language),
            )
            _save_reminder_message(telegram_id, medication_id, sent.message_id)

            repeat_minutes = settings.REMINDER_RETRY_MINUTES
            if user_settings:
                repeat_minutes = user_settings.reminder_repeat_minutes

            next_followup_time = datetime.now(tz) + timedelta(minutes=repeat_minutes)
            next_job_id = f"followup_{medication_id}_{int(next_followup_time.timestamp())}"

            scheduler.add_job(
                send_followup_reminder,
                DateTrigger(run_date=next_followup_time),
                args=[bot, telegram_id, medication_id],
                id=next_job_id,
                replace_existing=True,
            )

            logger.info(
                "Sent follow-up for %s, next in %s min",
                medication.name,
                repeat_minutes,
            )

    except Exception as e:
        logger.error("Error sending follow-up reminder: %s", e, exc_info=e)
