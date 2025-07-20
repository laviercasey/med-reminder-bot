from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from database.models import User
from database.db import get_session
from utils.keyboards import get_admin_keyboard, get_admin_users_keyboard
from utils.states import AdminStates
from utils.logger import log_admin_action
from config.config import settings
from services.admin import (
    get_admin_statistics, ban_user, unban_user, 
    extend_subscription, get_admin_logs, export_users_csv
)
import csv
import io

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Handle admin command - only accessible to admins"""
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        return
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            language = "en"
        else:
            language = user.language
    
    # Show admin panel
    await message.answer(
        "Admin panel",
        reply_markup=get_admin_keyboard(language)
    )
    
    log_admin_action(user_id, "opened_admin_panel")

@router.callback_query(F.data == "admin:stats")
async def admin_show_stats(callback: types.CallbackQuery):
    """Show admin statistics"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        language = user.language if user else "en"
    
    # Get statistics
    stats = await get_admin_statistics()
    
    # Format message
    message_text = f"""
📊 Bot Statistics:

👥 Total users: {stats['total_users']}
👤 Active users (7 days): {stats['active_users']}
⭐ Premium users: {stats['premium_users']}
💊 Average medications per user: {stats['avg_pills']}
💰 Monthly income: {stats['monthly_income']} RUB
"""
    
    await callback.message.edit_text(
        message_text,
        reply_markup=get_admin_keyboard(language)
    )
    
    log_admin_action(user_id, "viewed_stats")
    await callback.answer()

@router.callback_query(F.data == "admin:users")
async def admin_manage_users(callback: types.CallbackQuery):
    """Show user management options"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    await callback.message.edit_text(
        "User Management\n\nSelect an action:",
        reply_markup=get_admin_users_keyboard()
    )
    
    log_admin_action(user_id, "opened_user_management")
    await callback.answer()

@router.callback_query(F.data == "admin:ban")
async def admin_ban_user_start(callback: types.CallbackQuery, state: FSMContext):
    """Start ban user process"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    await callback.message.edit_text("Enter the Telegram ID of the user to ban:")
    await state.set_state(AdminStates.waiting_for_user_id)
    await state.update_data(action="ban")
    
    log_admin_action(user_id, "started_ban_process")
    await callback.answer()

@router.callback_query(F.data == "admin:unban")
async def admin_unban_user_start(callback: types.CallbackQuery, state: FSMContext):
    """Start unban user process"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    await callback.message.edit_text("Enter the Telegram ID of the user to unban:")
    await state.set_state(AdminStates.waiting_for_user_id)
    await state.update_data(action="unban")
    
    log_admin_action(user_id, "started_unban_process")
    await callback.answer()

@router.callback_query(F.data == "admin:extend")
async def admin_extend_subscription_start(callback: types.CallbackQuery, state: FSMContext):
    """Start extend subscription process"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    await callback.message.edit_text("Enter the Telegram ID of the user to extend subscription:")
    await state.set_state(AdminStates.waiting_for_user_id)
    await state.update_data(action="extend")
    
    log_admin_action(user_id, "started_extend_subscription_process")
    await callback.answer()

@router.message(AdminStates.waiting_for_user_id)
async def process_user_id_input(message: types.Message, state: FSMContext):
    """Process user ID input for admin actions"""
    admin_id = message.from_user.id
    
    # Check if user is admin
    if admin_id not in settings.ADMIN_IDS:
        return
    
    # Get action from state
    state_data = await state.get_data()
    action = state_data.get("action")
    
    try:
        target_user_id = int(message.text.strip())
    except ValueError:
        await message.answer("Invalid user ID. Please enter a valid numeric ID.")
        return
    
    if action == "ban":
        # Ban user
        success = await ban_user(admin_id, target_user_id)
        
        if success:
            await message.answer(f"User {target_user_id} has been banned.")
            log_admin_action(admin_id, "banned_user", target_user_id)
        else:
            await message.answer(f"User {target_user_id} not found.")
        
        await state.clear()
    
    elif action == "unban":
        # Unban user
        success = await unban_user(admin_id, target_user_id)
        
        if success:
            await message.answer(f"User {target_user_id} has been unbanned.")
            log_admin_action(admin_id, "unbanned_user", target_user_id)
        else:
            await message.answer(f"User {target_user_id} not found.")
        
        await state.clear()
    
    elif action == "extend":
        # Store target user ID and ask for number of days
        await state.update_data(target_user_id=target_user_id)
        await message.answer("Enter the number of days to extend the subscription:")
        await state.set_state(AdminStates.waiting_for_days)
    
    else:
        await state.clear()

@router.message(AdminStates.waiting_for_days)
async def process_days_input(message: types.Message, state: FSMContext):
    """Process days input for subscription extension"""
    admin_id = message.from_user.id
    
    # Check if user is admin
    if admin_id not in settings.ADMIN_IDS:
        return
    
    # Get target user ID from state
    state_data = await state.get_data()
    target_user_id = state_data.get("target_user_id")
    
    try:
        days = int(message.text.strip())
        if days <= 0:
            raise ValueError("Days must be positive")
    except ValueError:
        await message.answer("Invalid input. Please enter a positive number of days.")
        return
    
    # Extend subscription
    success = await extend_subscription(admin_id, target_user_id, days)
    
    if success:
        await message.answer(f"Subscription for user {target_user_id} extended by {days} days.")
        log_admin_action(admin_id, "extended_subscription", target_user_id)
    else:
        await message.answer(f"User {target_user_id} not found.")
    
    await state.clear()

@router.callback_query(F.data == "admin:logs")
async def admin_show_logs(callback: types.CallbackQuery):
    """Show admin logs and reports"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        language = user.language if user else "en"
    
    # Create reports keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Export Users (CSV)", callback_data="admin:export_users")],
        [types.InlineKeyboardButton(text="Back", callback_data="admin:back")]
    ])
    
    await callback.message.edit_text(
        "Logs and Reports\n\nSelect a report to generate:",
        reply_markup=keyboard
    )
    
    log_admin_action(user_id, "opened_logs_and_reports")
    await callback.answer()

@router.callback_query(F.data == "admin:export_users")
async def admin_export_users(callback: types.CallbackQuery):
    """Export users to CSV"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    # Get CSV data
    csv_data = await export_users_csv()
    
    # Create file-like object
    file_obj = io.BytesIO(csv_data.encode('utf-8'))
    file_obj.name = "users_export.csv"
    
    # Send file
    await callback.message.answer_document(
        document=types.BufferedInputFile(
            file_obj.getvalue(),
            filename="users_export.csv"
        )
    )
    
    log_admin_action(user_id, "exported_users_csv")
    await callback.answer()

@router.callback_query(F.data == "admin:back")
async def admin_back_to_main(callback: types.CallbackQuery):
    """Return to admin main menu"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        language = user.language if user else "en"
    
    await callback.message.edit_text(
        "Admin panel",
        reply_markup=get_admin_keyboard(language)
    )
    
    await callback.answer()
