import logging
from datetime import UTC, datetime

from aiogram import F, Router, types
from aiogram.filters import Command
from sqlalchemy import select

from bot.keyboards import get_language_keyboard
from bot.localization import get_text
from shared.database.db import get_session
from shared.database.models import User

router = Router()
logger = logging.getLogger("med_reminder_bot")


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    user_id = message.from_user.id

    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        existing_user = (await session.execute(user_query)).scalar_one_or_none()

        if existing_user:
            existing_user.last_active = datetime.now(UTC)
            await session.commit()

            if existing_user.is_blocked:
                await message.answer(get_text("user_blocked", existing_user.language))
                return

            await message.answer(
                get_text("welcome", existing_user.language),
            )
            logger.info("User %s: start_command - returning user", user_id)
        else:
            await message.answer(
                get_text("select_language", "en"),
                reply_markup=get_language_keyboard(),
            )
            logger.info("User %s: start_command - new user", user_id)


SUPPORTED_LANGUAGES = frozenset({"ru", "en"})


@router.callback_query(F.data.startswith("language:"))
async def process_language_selection(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id
    selected_language = callback.data.split(":")[1]

    if selected_language not in SUPPORTED_LANGUAGES:
        await callback.answer()
        return

    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        existing_user = (await session.execute(user_query)).scalar_one_or_none()

        if existing_user:
            existing_user.language = selected_language
            existing_user.last_active = datetime.now(UTC)
        else:
            new_user = User(
                telegram_id=user_id,
                language=selected_language,
                created_at=datetime.now(UTC),
                last_active=datetime.now(UTC),
            )
            session.add(new_user)

        await session.commit()

    welcome_text = get_text("language_selected", selected_language)

    await callback.message.edit_text(welcome_text)

    await callback.message.answer(
        get_text("welcome", selected_language),
    )

    logger.info("User %s: language_selected - %s", user_id, selected_language)
    await callback.answer()
