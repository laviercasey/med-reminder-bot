from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, update
from database.models import User
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_language_keyboard, get_main_menu_keyboard, get_settings_keyboard, get_reminder_settings_keyboard
from utils.states import SettingsStates
from utils.logger import log_user_action

router = Router()

@router.message(Command("settings"))
@router.message(F.text.func(lambda text: text in ["Настройки", "Settings"]))
async def cmd_settings(message: types.Message):
    """Handle settings command"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Send settings menu
        await message.answer(
            get_text("settings", user.language),
            reply_markup=get_settings_keyboard(user.language)
        )
        
        log_user_action(user_id, "opened_settings")

@router.callback_query(F.data == "settings:language")
async def settings_change_language(callback: types.CallbackQuery, state: FSMContext):
    """Handle language change in settings"""
    await callback.message.edit_text(
        get_text("select_language", "en"),
        reply_markup=get_language_keyboard()
    )
    
    await callback.answer()
    
    # Set state to wait for language selection
    await state.set_state(SettingsStates.waiting_for_language)

@router.callback_query(SettingsStates.waiting_for_language, F.data.startswith("language:"))
async def process_settings_language_selection(callback: types.CallbackQuery, state: FSMContext):
    """Process language selection in settings"""
    user_id = callback.from_user.id
    selected_language = callback.data.split(":")[1]  # "language:en" -> "en"
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Update user's language
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(language=selected_language)
        )
        
        await session.commit()
    
    # Send confirmation
    await callback.message.edit_text(
        get_text("language_selected", selected_language)
    )
    
    # Return to main menu with updated language
    await callback.message.answer(
        get_text("main_menu", selected_language),
        reply_markup=get_main_menu_keyboard(selected_language)
    )
    
    # Clear state
    await state.clear()
    
    log_user_action(user_id, "changed_language", selected_language)
    await callback.answer()



@router.callback_query(F.data == "settings:reminders")
async def settings_reminders(callback: types.CallbackQuery):
    """Handle reminder settings"""
    user_id = callback.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get user settings or create if not exists
        from database.models import UserSettings
        
        settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
        user_settings = (await session.execute(settings_query)).scalar_one_or_none()
        
        if not user_settings:
            user_settings = UserSettings(
                user_id=user.id,
                reminders_enabled=True,
                reminder_repeat_minutes=30
            )
            session.add(user_settings)
            await session.commit()
        
        # Create message
        message_text = get_text("reminder_settings", user.language) + "\n\n"
        
        if user_settings.reminders_enabled:
            message_text += get_text("reminders_enabled", user.language)
        else:
            message_text += get_text("reminders_disabled", user.language)
        
        message_text += "\n" + get_text("reminder_repeat_time", user.language) + f" {user_settings.reminder_repeat_minutes} " + get_text("minutes", user.language, default="minutes")
        
        # Send message with settings keyboard
        await callback.message.edit_text(
            message_text,
            reply_markup=get_reminder_settings_keyboard(user.language, user_settings.reminders_enabled)
        )
        
        log_user_action(user_id, "viewed_reminder_settings")
        await callback.answer()

@router.callback_query(F.data.startswith("reminder_settings:"))
async def process_reminder_settings(callback: types.CallbackQuery):
    """Process reminder settings changes"""
    user_id = callback.from_user.id
    action = callback.data.split(":")[1]  # "enable" or "disable"
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get user settings
        from database.models import UserSettings
        
        settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
        user_settings = (await session.execute(settings_query)).scalar_one_or_none()
        
        if not user_settings:
            user_settings = UserSettings(
                user_id=user.id,
                reminders_enabled=True,
                reminder_repeat_minutes=30
            )
            session.add(user_settings)
        
        # Update settings
        if action == "enable":
            user_settings.reminders_enabled = True
        elif action == "disable":
            user_settings.reminders_enabled = False
        
        await session.commit()
        
        # Update message
        message_text = get_text("reminder_settings", user.language) + "\n\n"
        
        if user_settings.reminders_enabled:
            message_text += get_text("reminders_enabled", user.language)
        else:
            message_text += get_text("reminders_disabled", user.language)
        
        message_text += "\n" + get_text("reminder_repeat_time", user.language) + f" {user_settings.reminder_repeat_minutes} " + get_text("minutes", user.language, default="minutes")
        
        # Send message with updated settings keyboard
        await callback.message.edit_text(
            message_text,
            reply_markup=get_reminder_settings_keyboard(user.language, user_settings.reminders_enabled)
        )
        
        log_user_action(user_id, f"reminders_{action}d")
        await callback.answer(get_text("reminder_settings_updated", user.language))

@router.callback_query(F.data.startswith("reminder_repeat:"))
async def process_reminder_repeat(callback: types.CallbackQuery):
    """Process reminder repeat time changes"""
    user_id = callback.from_user.id
    minutes = int(callback.data.split(":")[1])  # 5, 15, or 30
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get user settings
        from database.models import UserSettings
        
        settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
        user_settings = (await session.execute(settings_query)).scalar_one_or_none()
        
        if not user_settings:
            user_settings = UserSettings(
                user_id=user.id,
                reminders_enabled=True,
                reminder_repeat_minutes=minutes
            )
            session.add(user_settings)
        else:
            user_settings.reminder_repeat_minutes = minutes
        
        await session.commit()
        
        # Update message
        message_text = get_text("reminder_settings", user.language) + "\n\n"
        
        if user_settings.reminders_enabled:
            message_text += get_text("reminders_enabled", user.language)
        else:
            message_text += get_text("reminders_disabled", user.language)
        
        message_text += "\n" + get_text("reminder_repeat_time", user.language) + f" {user_settings.reminder_repeat_minutes} " + get_text("minutes", user.language, default="minutes")
        
        # Send message with updated settings keyboard
        await callback.message.edit_text(
            message_text,
            reply_markup=get_reminder_settings_keyboard(user.language, user_settings.reminders_enabled)
        )
        
        log_user_action(user_id, f"reminder_repeat_set_to_{minutes}")
        await callback.answer(get_text("reminder_settings_updated", user.language))
