import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.handlers import setup_routers
from bot.services.pubsub import RedisPubSubListener
from bot.services.reminders import setup_daily_reminders
from shared.config import settings
from shared.database.db import configure_engine, get_session, init_db
from shared.logging import setup_logger

logger = setup_logger("med_reminder_bot")


async def main() -> None:

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = RedisStorage.from_url(settings.REDIS_URL)
    dp = Dispatcher(storage=storage)

    dp.include_router(setup_routers())

    configure_engine(settings.database_url)

    logger.info("Initializing database...")
    await init_db()

    async with get_session() as session:
        from sqlalchemy import select

        from shared.database.models import User, UserSettings

        query = select(User).where(~User.id.in_(select(UserSettings.user_id)))
        users_without_settings = (await session.execute(query)).scalars().all()

        for user in users_without_settings:
            user_settings = UserSettings(
                user_id=user.id,
                reminders_enabled=True,
                reminder_repeat_minutes=30,
            )
            session.add(user_settings)

        await session.commit()

    await setup_daily_reminders(bot)

    pubsub_listener = RedisPubSubListener(bot)
    await pubsub_listener.start()

    logger.info("Bot started")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await pubsub_listener.stop()
        await storage.close()


if __name__ == "__main__":
    asyncio.run(main())
