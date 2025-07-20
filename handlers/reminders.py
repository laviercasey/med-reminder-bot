from aiogram import Router, F, types
from aiogram.filters import Command
from sqlalchemy import select, update
from database.models import User, Medication, Checklist, UserSettings
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_snooze_options_keyboard
from utils.logger import log_user_action
from datetime import datetime, timedelta
from services.reminders import setup_daily_reminders
from services.payments import is_premium_active

router = Router()

@router.callback_query(F.data.startswith("snooze:"))
async def process_snooze(callback: types.CallbackQuery):
    """Process snooze request"""
    user_id = callback.from_user.id
    
    # Check if this is a snooze option selection
    parts = callback.data.split(":")
    if len(parts) == 3:
        # This is a snooze time selection
        checklist_id = int(parts[1])
        minutes = int(parts[2])
        
        async with get_session() as session:
            user_query = select(User).where(User.telegram_id == user_id)
            user = (await session.execute(user_query)).scalar_one_or_none()
            
            if not user or user.is_blocked:
                await callback.answer()
                return
            
            # Get the checklist and medication
            checklist_query = select(Checklist, Medication).join(
                Medication, Checklist.medication_id == Medication.id
            ).where(
                Checklist.id == checklist_id,
                Checklist.user_id == user.id
            )
            
            result = await session.execute(checklist_query)
            checklist_data = result.first()
            
            if not checklist_data:
                await callback.answer(get_text("error", user.language, default="Error occurred"))
                return
            
            checklist, medication = checklist_data
            
            # Schedule a one-time reminder
            from apscheduler.triggers.date import DateTrigger
            from services.reminders import scheduler, send_medication_reminder
            
            # Calculate snooze time
            snooze_time = datetime.now() + timedelta(minutes=minutes)
            
            # Create a one-time job for this reminder
            job_id = f"snooze_{checklist.id}_{int(snooze_time.timestamp())}"
            
            scheduler.add_job(
                send_medication_reminder,
                DateTrigger(run_date=snooze_time),
                args=[callback.bot, user_id, medication.id],
                id=job_id,
                replace_existing=True
            )
            
            # Confirm snooze
            await callback.message.edit_text(
                get_text("snoozed_for", user.language, minutes=minutes)
            )
            
            log_user_action(user_id, "snoozed_reminder", f"{medication.name} for {minutes} minutes")
            await callback.answer()
        
    else:
        # This is the initial snooze button press
        checklist_id = int(parts[1])
        
        async with get_session() as session:
            user_query = select(User).where(User.telegram_id == user_id)
            user = (await session.execute(user_query)).scalar_one_or_none()
            
            if not user or user.is_blocked:
                await callback.answer()
                return
            
            # Ask for snooze duration
            await callback.message.edit_text(
                get_text("select_snooze_time", user.language, default="Select snooze time:"),
                reply_markup=get_snooze_options_keyboard(checklist_id, user.language)
            )
            
            await callback.answer()

@router.callback_query(F.data.startswith("disable_reminder:"))
async def disable_reminder(callback: types.CallbackQuery):
    """Disable a specific reminder"""
    user_id = callback.from_user.id
    checklist_id = int(callback.data.split(":")[1])
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Mark the checklist item as taken to prevent further reminders
        await session.execute(
            update(Checklist)
            .where(Checklist.id == checklist_id, Checklist.user_id == user.id)
            .values(status=True)
        )
        
        await session.commit()
        
        # Update the message
        await callback.message.edit_text(
            get_text("reminder_disabled", user.language)
        )
        
        log_user_action(user_id, "disabled_reminder", f"checklist_id: {checklist_id}")
        await callback.answer()
