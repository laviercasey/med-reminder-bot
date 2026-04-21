import logging
from datetime import datetime, timedelta

from aiogram import F, Router, types
from sqlalchemy import select, update

from bot.keyboards import get_snooze_options_keyboard
from bot.localization import get_text
from shared.database.db import get_session
from shared.database.models import Checklist, Medication, User, UserSettings

router = Router()
logger = logging.getLogger("med_reminder_bot")


def _cancel_followups_for_medication(medication_id: int) -> None:
    from bot.services.reminders import scheduler

    jobs_to_remove = [
        j.id for j in scheduler.get_jobs() if j.id.startswith(f"followup_{medication_id}_")
    ]
    for job_id in jobs_to_remove:
        try:
            scheduler.remove_job(job_id)
            logger.info("Cancelled followup: %s", job_id)
        except Exception:
            pass


def _cancel_all_pending_for_checklist(checklist_id: int, medication_id: int) -> None:
    from bot.services.reminders import scheduler

    jobs_to_remove = [
        j.id
        for j in scheduler.get_jobs()
        if j.id.startswith(f"followup_{medication_id}_")
        or j.id.startswith(f"snooze_{checklist_id}_")
    ]
    for job_id in jobs_to_remove:
        try:
            scheduler.remove_job(job_id)
            logger.info("Cancelled job: %s", job_id)
        except Exception:
            pass


@router.callback_query(F.data.startswith("snooze:"))
async def process_snooze(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id
    parts = callback.data.split(":")

    if len(parts) == 3:
        try:
            checklist_id = int(parts[1])
            minutes = int(parts[2])
        except ValueError:
            await callback.answer()
            return

        async with get_session() as session:
            user_query = select(User).where(User.telegram_id == user_id)
            user = (await session.execute(user_query)).scalar_one_or_none()

            if not user or user.is_blocked:
                await callback.answer()
                return

            checklist_query = (
                select(Checklist, Medication)
                .join(Medication, Checklist.medication_id == Medication.id)
                .where(Checklist.id == checklist_id, Checklist.user_id == user.id)
            )

            result = await session.execute(checklist_query)
            checklist_data = result.first()

            if not checklist_data:
                await callback.answer(get_text("error", user.language))
                return

            checklist, medication = checklist_data

            _cancel_followups_for_medication(medication.id)

            from apscheduler.triggers.date import DateTrigger

            from bot.services.reminders import _get_user_tz, scheduler, send_followup_reminder

            settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
            user_settings = (await session.execute(settings_query)).scalar_one_or_none()
            tz = _get_user_tz(user_settings)

            snooze_time = datetime.now(tz) + timedelta(minutes=minutes)
            job_id = f"snooze_{checklist.id}_{int(snooze_time.timestamp())}"

            scheduler.add_job(
                send_followup_reminder,
                DateTrigger(run_date=snooze_time),
                args=[callback.bot, user_id, medication.id],
                id=job_id,
                replace_existing=True,
            )

            await callback.message.edit_text(
                get_text("snoozed_for", user.language, minutes=minutes)
            )

            logger.info(
                "User %s: snoozed_reminder - %s for %s minutes",
                user_id,
                medication.name,
                minutes,
            )
            await callback.answer()
    else:
        try:
            checklist_id = int(parts[1])
        except ValueError:
            await callback.answer()
            return

        async with get_session() as session:
            user_query = select(User).where(User.telegram_id == user_id)
            user = (await session.execute(user_query)).scalar_one_or_none()

            if not user or user.is_blocked:
                await callback.answer()
                return

            await callback.message.edit_text(
                get_text("select_snooze_time", user.language),
                reply_markup=get_snooze_options_keyboard(checklist_id, user.language),
            )

            await callback.answer()


@router.callback_query(F.data.startswith("disable_reminder:"))
async def disable_reminder(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id
    try:
        checklist_id = int(callback.data.split(":")[1])
    except (ValueError, IndexError):
        await callback.answer()
        return

    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()

        if not user or user.is_blocked:
            await callback.answer()
            return

        checklist_query = (
            select(Checklist, Medication)
            .join(Medication, Checklist.medication_id == Medication.id)
            .where(Checklist.id == checklist_id, Checklist.user_id == user.id)
        )
        result = await session.execute(checklist_query)
        checklist_data = result.first()

        if checklist_data:
            checklist, medication = checklist_data
            _cancel_all_pending_for_checklist(checklist.id, medication.id)

        await session.execute(
            update(Checklist)
            .where(Checklist.id == checklist_id, Checklist.user_id == user.id)
            .values(status=True)
        )

        await session.commit()

        await callback.message.edit_text(get_text("reminder_disabled", user.language))

        logger.info("User %s: disabled_reminder - checklist_id: %s", user_id, checklist_id)
        await callback.answer()


@router.callback_query(F.data.startswith("mark_taken:"))
async def process_mark_as_taken(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id
    try:
        checklist_id = int(callback.data.split(":")[1])
    except (ValueError, IndexError):
        await callback.answer()
        return

    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()

        if not user or user.is_blocked:
            await callback.answer()
            return

        checklist_query = (
            select(Checklist, Medication)
            .join(Medication, Checklist.medication_id == Medication.id)
            .where(Checklist.id == checklist_id, Checklist.user_id == user.id)
        )

        result = await session.execute(checklist_query)
        checklist_data = result.first()

        if not checklist_data:
            await callback.answer()
            return

        checklist, medication = checklist_data

        _cancel_all_pending_for_checklist(checklist.id, medication.id)

        await session.execute(
            update(Checklist)
            .where(Checklist.id == checklist_id, Checklist.user_id == user.id)
            .values(status=True)
        )

        await session.commit()

        await callback.message.edit_text(
            f"✅ {medication.name} - {medication.time.strftime('%H:%M')}"
        )

        await callback.answer(get_text("marked_as_taken", user.language, name=medication.name))

        logger.info("User %s: marked_pill_taken - %s", user_id, medication.name)
