import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import settings
from handlers import setup_routers
from database.db import init_db
from services.reminders import setup_daily_reminders
from utils.logger import log_info
from database.db import get_session

async def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize bot and dispatcher
    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Setup handlers
    dp.include_router(setup_routers())
    
    # Initialize database
    log_info("Initializing database...")
    await init_db()
    
    # Initialize user settings for existing users
    async with get_session() as session:
        from database.models import User, UserSettings
        from sqlalchemy import select
        
        # Get all users without settings
        query = select(User).where(
            ~User.id.in_(select(UserSettings.user_id))
        )
        
        users_without_settings = (await session.execute(query)).scalars().all()
        
        # Create default settings for these users
        for user in users_without_settings:
            user_settings = UserSettings(
                user_id=user.id,
                reminders_enabled=True,
                reminder_repeat_minutes=30
            )
            session.add(user_settings)
        
        await session.commit()
    
    # Setup reminders
    await setup_daily_reminders(bot)

    # Start polling
    log_info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
