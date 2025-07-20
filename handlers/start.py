from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from database.models import User
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_language_keyboard, get_main_menu_keyboard
from utils.logger import log_user_action
from datetime import datetime, timedelta

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        # Check if user already exists
        user_query = select(User).where(User.telegram_id == user_id)
        existing_user = (await session.execute(user_query)).scalar_one_or_none()
        
        if existing_user:
            # User exists, update last_active
            existing_user.last_active = datetime.utcnow()
            await session.commit()
            
            # Check if user is blocked
            if existing_user.is_blocked:
                await message.answer(get_text("user_blocked", existing_user.language))
                return
            
            premium_status = get_text(
                "premium_status_active" if existing_user.is_premium 
                else "premium_status_inactive", 
                existing_user.language
            )
            
            # Send welcome back message
            await message.answer(
                f"{get_text('welcome', existing_user.language)}\n\n{premium_status}",
                reply_markup=get_main_menu_keyboard(existing_user.language)
            )
            log_user_action(user_id, "start_command", "returning user")
            
        else:
            # New user, ask for language preference
            await message.answer(
                get_text("select_language", "en"),
                reply_markup=get_language_keyboard()
            )
            log_user_action(user_id, "start_command", "new user")

@router.callback_query(F.data.startswith("language:"))
async def process_language_selection(callback: types.CallbackQuery):
    """Process language selection callback"""
    user_id = callback.from_user.id
    selected_language = callback.data.split(":")[1]  # "language:en" -> "en"
    
    async with get_session() as session:
        # Check if user already exists
        user_query = select(User).where(User.telegram_id == user_id)
        existing_user = (await session.execute(user_query)).scalar_one_or_none()
        
        if existing_user:
            # Update existing user's language
            existing_user.language = selected_language
            existing_user.last_active = datetime.utcnow()
        else:
            # Create new user
            new_user = User(
                telegram_id=user_id,
                language=selected_language,
                created_at=datetime.now(),
                last_active=datetime.now(),
                is_premium=True,
                premium_until=datetime.now() + timedelta(days=30)
            )
            session.add(new_user)
        
        await session.commit()

    
    
    welcome_text = (
        f"{get_text('language_selected', selected_language)}\n"
        f"{get_text('trial_activated', selected_language)}")
    
    # Send confirmation and main menu
    await callback.message.edit_text(
        welcome_text
    )
    
    await callback.message.answer(
        get_text("welcome", selected_language),
        reply_markup=get_main_menu_keyboard(selected_language)  
    )
    
    log_user_action(user_id, "language_selected", selected_language)
    await callback.answer()
