from datetime import datetime, timedelta
from sqlalchemy import select, and_
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.models import User, Medication, Checklist
from database.db import get_session
from aiogram import Bot
from utils.localization import get_text
from utils.keyboards import get_checklist_keyboard, get_subscription_keyboard, get_reminder_action_keyboard
from utils.logger import log_info, log_error
from config.config import settings
from services.payments import is_premium_active
import asyncio

scheduler = AsyncIOScheduler()

async def setup_daily_reminders(bot: Bot):
    """Setup daily reminder jobs"""
    log_info("Setting up daily reminder jobs")
    
    # Clear existing jobs
    scheduler.remove_all_jobs()
    
    # Add job to generate daily checklists
    scheduler.add_job(
        generate_daily_checklists,
        CronTrigger(hour=0, minute=1),  # Run at 00:01 every day
        args=[bot],
        id="generate_checklists"
    )
    
    # Add job to check for expiring subscriptions
    scheduler.add_job(
        check_expiring_subscriptions,
        CronTrigger(hour=12, minute=0),  # Run at 12:00 every day
        args=[bot],
        id="check_subscriptions"
    )
    
    # Setup individual reminder jobs for each user's medications
    await setup_medication_reminders(bot)
    
    # Start the scheduler
    if not scheduler.running:
        scheduler.start()

async def setup_medication_reminders(bot: Bot):
    """Setup reminder jobs for all users' medications"""
    log_info("Setting up medication reminders")
    
    async with get_session() as session:
        # Get all active users and their medications
        query = select(User, Medication).join(
            Medication, User.id == Medication.user_id
        ).where(User.is_blocked == False)
        
        result = await session.execute(query)
        
        for user, medication in result:
            hour = medication.time.hour
            minute = medication.time.minute
            
            job_id = f"reminder_{medication.id}"
            
            # Remove existing job if it exists
            if scheduler.get_job(job_id):
                scheduler.remove_job(job_id)
            
            # Add new reminder job
            scheduler.add_job(
                send_medication_reminder,
                CronTrigger(hour=hour, minute=minute),
                args=[bot, user.telegram_id, medication.id],
                id=job_id
            )
            
            # Add follow-up reminder if needed
            followup_job_id = f"followup_{medication.id}"
            if scheduler.get_job(followup_job_id):
                scheduler.remove_job(followup_job_id)
                
            followup_hour = hour
            followup_minute = minute + settings.REMINDER_RETRY_MINUTES
            
            if followup_minute >= 60:
                followup_hour = (hour + followup_minute // 60) % 24
                followup_minute = followup_minute % 60
            
            scheduler.add_job(
                send_followup_reminder,
                CronTrigger(hour=followup_hour, minute=followup_minute),
                args=[bot, user.telegram_id, medication.id],
                id=followup_job_id
            )

async def generate_daily_checklists(bot: Bot):
    """Generate daily checklists for all users"""
    log_info("Generating daily checklists")
    today = datetime.now().date()
    
    async with get_session() as session:
        # Get all active users and their medications
        query = select(User, Medication).join(
            Medication, User.id == Medication.user_id
        ).where(User.is_blocked == False)
        
        result = await session.execute(query)
        user_medications = {}
        
        for user, medication in result:
            if user.id not in user_medications:
                user_medications[user.id] = []
            user_medications[user.id].append(medication)
        
        # Create checklist items for each user's medications
        for user_id, medications in user_medications.items():
            for medication in medications:
                # Check if checklist item already exists
                checklist_query = select(Checklist).where(
                    Checklist.user_id == user_id,
                    Checklist.medication_id == medication.id,
                    Checklist.date == today
                )
                
                checklist_exists = await session.execute(checklist_query)
                if checklist_exists.first() is None:  # Исправлено условие проверки
                    # Create new checklist item
                    new_checklist = Checklist(
                        user_id=user_id,
                        medication_id=medication.id,
                        date=today,
                        status=False
                    )
                    session.add(new_checklist)
        
        await session.commit()


async def send_medication_reminder(bot: Bot, telegram_id: int, medication_id: int):
    """Send a reminder to take medication"""
    try:
        async with get_session() as session:
            # Get user and medication info
            user_query = select(User).where(User.telegram_id == telegram_id)
            user = (await session.execute(user_query)).scalar_one_or_none()
            
            if not user or user.is_blocked:
                return
            
            # Check if reminders are enabled for this user
            from database.models import UserSettings
            
            settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
            user_settings = (await session.execute(settings_query)).scalar_one_or_none()
            
            # If user has settings and reminders are disabled, don't send reminder
            if user_settings and not user_settings.reminders_enabled:
                return
            
            medication_query = select(Medication).where(Medication.id == medication_id)
            medication = (await session.execute(medication_query)).scalar_one_or_none()
            
            if not medication:
                return
            
            # Get today's checklist item
            today = datetime.now().date()
            checklist_query = select(Checklist).where(
                Checklist.user_id == user.id,
                Checklist.medication_id == medication_id,
                Checklist.date == today
            )
            
            checklist = (await session.execute(checklist_query)).scalar_one_or_none()
            
            # If already taken, don't send reminder
            if checklist and checklist.status:
                return
            
            # Create checklist item if it doesn't exist
            if not checklist:
                checklist = Checklist(
                    user_id=user.id,
                    medication_id=medication_id,
                    date=today,
                    status=False
                )
                session.add(checklist)
                await session.commit()
                checklist_id = checklist.id
            else:
                checklist_id = checklist.id
            
            # Send reminder message
            reminder_text = get_text("reminder", user.language, name=medication.name)
            
            # Add ad banner for non-premium users
            is_premium = await is_premium_active(user)
            if not is_premium:
                ad_text = "\n\n" + get_text("ad_banner", user.language)
                reminder_text += ad_text
            
            await bot.send_message(
                chat_id=telegram_id,
                text=reminder_text,
                reply_markup=get_reminder_action_keyboard(checklist_id, user.language)
            )
    
    except Exception as e:
        log_error(f"Error sending reminder: {e}", exc_info=e)

async def send_followup_reminder(bot: Bot, telegram_id: int, medication_id: int):
    """Send a follow-up reminder if medication hasn't been marked as taken"""
    try:
        async with get_session() as session:
            # Get user and medication info
            user_query = select(User).where(User.telegram_id == telegram_id)
            user = (await session.execute(user_query)).scalar_one_or_none()
            
            if not user or user.is_blocked:
                return
            
            # Check if reminders are enabled for this user
            from database.models import UserSettings
            
            settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
            user_settings = (await session.execute(settings_query)).scalar_one_or_none()
            
            # If user has settings and reminders are disabled, don't send reminder
            if user_settings and not user_settings.reminders_enabled:
                return
            
            medication_query = select(Medication).where(Medication.id == medication_id)
            medication = (await session.execute(medication_query)).scalar_one_or_none()
            
            if not medication:
                return
            
            # Get today's checklist item
            today = datetime.now().date()
            checklist_query = select(Checklist).where(
                Checklist.user_id == user.id,
                Checklist.medication_id == medication_id,
                Checklist.date == today
            )
            
            checklist = (await session.execute(checklist_query)).scalar_one_or_none()
            
            # If already taken or checklist doesn't exist, don't send reminder
            if not checklist or checklist.status:
                return
            
            # Send follow-up reminder message
            reminder_text = get_text("reminder_repeat", user.language, name=medication.name)
            
            # Add ad banner for non-premium users
            is_premium = await is_premium_active(user)
            if not is_premium:
                ad_text = "\n\n" + get_text("ad_banner", user.language)
                reminder_text += ad_text
            
            await bot.send_message(
                chat_id=telegram_id,
                text=reminder_text,
                reply_markup=get_reminder_action_keyboard(checklist.id, user.language)
            )
    
    except Exception as e:
        log_error(f"Error sending follow-up reminder: {e}", exc_info=e)

async def setup_medication_reminders(bot: Bot):
    """Setup reminder jobs for all users' medications"""
    log_info("Setting up medication reminders")
    
    async with get_session() as session:
        # Get all active users and their medications
        query = select(User, Medication).join(
            Medication, User.id == Medication.user_id
        ).where(User.is_blocked == False)
        
        result = await session.execute(query)
        
        for user, medication in result:
            hour = medication.time.hour
            minute = medication.time.minute
            
            job_id = f"reminder_{medication.id}"
            
            # Remove existing job if it exists
            if scheduler.get_job(job_id):
                scheduler.remove_job(job_id)
            
            # Add new reminder job
            scheduler.add_job(
                send_medication_reminder,
                CronTrigger(hour=hour, minute=minute),
                args=[bot, user.telegram_id, medication.id],
                id=job_id
            )
            
            # Get user settings
            from database.models import UserSettings
            
            settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
            user_settings = (await session.execute(settings_query)).scalar_one_or_none()
            
            # Default repeat time
            repeat_minutes = 30
            
            if user_settings:
                repeat_minutes = user_settings.reminder_repeat_minutes
            
            # Add follow-up reminder if needed
            followup_job_id = f"followup_{medication.id}"
            if scheduler.get_job(followup_job_id):
                scheduler.remove_job(followup_job_id)
                
            followup_hour = hour
            followup_minute = minute + repeat_minutes
            
            if followup_minute >= 60:
                followup_hour = (hour + followup_minute // 60) % 24
                followup_minute = followup_minute % 60
            
            scheduler.add_job(
                send_followup_reminder,
                CronTrigger(hour=followup_hour, minute=followup_minute),
                args=[bot, user.telegram_id, medication.id],
                id=followup_job_id
            )

async def check_expiring_subscriptions(bot: Bot):
    """Check for subscriptions expiring tomorrow and send notifications"""
    log_info("Checking for expiring subscriptions")
    tomorrow = datetime.now().date() + timedelta(days=1)
    tomorrow_start = datetime.combine(tomorrow, datetime.min.time())
    tomorrow_end = datetime.combine(tomorrow, datetime.max.time())
    
    async with get_session() as session:
        # Find users with subscriptions expiring tomorrow
        query = select(User).where(
            and_(
                User.is_premium == True,
                User.premium_until >= tomorrow_start,
                User.premium_until <= tomorrow_end
            )
        )
        
        result = await session.execute(query)
        expiring_users = result.scalars().all()
        
        for user in expiring_users:
            # Send expiration notification
            notification_text = get_text("subscription_expiring", user.language)
            
            await bot.send_message(
                chat_id=user.telegram_id,
                text=notification_text,
                reply_markup=get_subscription_keyboard(user.language)
            )
