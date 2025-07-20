from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, func
from database.models import User, Medication
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_schedule_keyboard, get_time_keyboard, get_main_menu_keyboard
from utils.states import AddPillStates
from utils.logger import log_user_action
from datetime import datetime, time
import re
from services.reminders import setup_medication_reminders  # Добавить этот импорт
from aiogram import Bot

router = Router()

@router.message(Command("add_pill"))
@router.message(F.text.func(lambda text: text in ["Добавить лекарство", "Add medication"]))
async def cmd_add_pill(message: types.Message, state: FSMContext):
    """Handle add pill command"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
         # Проверка лимита для обычных пользователей
        if not user.is_premium:
            count_query = (
                select(func.count())
                .select_from(Medication)
                .where(Medication.user_id == user.id)
            )
            med_count = (await session.execute(count_query)).scalar()
            
            if med_count >= 5:
                await message.answer(get_text("limit_reached", user.language))
                return

        # Ask for pill name
        await message.answer(get_text("enter_pill_name", user.language))
        await state.set_state(AddPillStates.waiting_for_name)
        
        # Store user language in state
        await state.update_data(language=user.language)
        
        log_user_action(user_id, "add_pill_command")

@router.message(AddPillStates.waiting_for_name)
async def process_pill_name(message: types.Message, state: FSMContext):
    """Process pill name input"""
    user_id = message.from_user.id
    pill_name = message.text.strip()
    
    if not pill_name:
        return
    
    # Store pill name in state
    await state.update_data(pill_name=pill_name)
    
    # Get user language from state
    state_data = await state.get_data()
    language = state_data.get("language", "en")
    
    # Ask for schedule
    await message.answer(
        get_text("select_schedule", language),
        reply_markup=get_schedule_keyboard(language)
    )
    
    await state.set_state(AddPillStates.waiting_for_schedule)
    
    log_user_action(user_id, "pill_name_entered", pill_name)

@router.callback_query(AddPillStates.waiting_for_schedule, F.data.startswith("schedule:"))
async def process_schedule_selection(callback: types.CallbackQuery, state: FSMContext):
    """Process schedule selection callback"""
    user_id = callback.from_user.id
    selected_schedule = callback.data.split(":")[1]  # "schedule:morning" -> "morning"
    
    # Store schedule in state
    await state.update_data(schedule=selected_schedule)
    
    # Get user language from state
    state_data = await state.get_data()
    language = state_data.get("language", "en")
    
    if selected_schedule == "custom":
        # Ask for custom time
        await callback.message.edit_text(get_text("enter_custom_time", language))
        await state.set_state(AddPillStates.waiting_for_custom_time)
    else:
        # Show time options for selected schedule
        await callback.message.edit_text(
            get_text("select_time", language),
            reply_markup=get_time_keyboard(selected_schedule, language)
        )
        await state.set_state(AddPillStates.waiting_for_time)
    
    log_user_action(user_id, "schedule_selected", selected_schedule)
    await callback.answer()

@router.callback_query(AddPillStates.waiting_for_time, F.data.startswith("time:"))
async def process_time_selection(callback: types.CallbackQuery, state: FSMContext,  bot: Bot):
    """Process time selection callback"""
    user_id = callback.from_user.id
    selected_time = callback.data.split(":")[1] + ":" + callback.data.split(":")[2]  # "time:08:00" -> "08:00"
    # Get state data
    state_data = await state.get_data()
    pill_name = state_data.get("pill_name")
    schedule = state_data.get("schedule")
    language = state_data.get("language", "en")
    
    # Parse time
    hour, minute = map(int, selected_time.split(":"))
    time_obj = time(hour=hour, minute=minute)
    
    # Save pill to database
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        new_medication = Medication(
            user_id=user.id,
            name=pill_name,
            schedule=schedule,
            time=time_obj
        )
        
        session.add(new_medication)
        await session.commit()
    
         # Получаем ID созданного лекарства
        medication_id = new_medication.id
        
        # Создаем запись в чеклисте на сегодня
        from database.models import Checklist
        from datetime import date
        
        today = date.today()
        
        # Проверяем, не существует ли уже такая запись
        checklist_query = select(Checklist).where(
            Checklist.user_id == user.id,
            Checklist.medication_id == medication_id,
            Checklist.date == today
        )
        existing_checklist = (await session.execute(checklist_query)).scalar_one_or_none()
        
        if not existing_checklist:
            # Создаем новую запись в чеклисте
            new_checklist = Checklist(
                user_id=user.id,
                medication_id=medication_id,
                date=today,
                status=False  # Лекарство еще не принято
            )
            session.add(new_checklist)
            await session.commit()

    # Confirm pill addition
    await callback.message.edit_text(
        get_text("pill_added", language, name=pill_name, time=selected_time)
    )
    
    await setup_medication_reminders(bot)
    
    # Clear state
    await state.clear()
    
    log_user_action(user_id, "pill_added", f"{pill_name} at {selected_time}")
    await callback.answer()

@router.message(AddPillStates.waiting_for_custom_time)
async def process_custom_time(message: types.Message, state: FSMContext, bot: Bot):
    """Process custom time input"""
    user_id = message.from_user.id
    time_input = message.text.strip()
    
    # Get state data
    state_data = await state.get_data()
    pill_name = state_data.get("pill_name")
    schedule = state_data.get("schedule")
    language = state_data.get("language", "en")
    
    # Validate time format (HH:MM)
    time_pattern = re.compile(r"^([01]?[0-9]|2[0-3]):([0-5][0-9])$")
    if not time_pattern.match(time_input):
        await message.answer(get_text("invalid_time_format", language))
        return
    
    # Parse time
    hour, minute = map(int, time_input.split(":"))
    time_obj = time(hour=hour, minute=minute)
    
    # Save pill to database
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        new_medication = Medication(
            user_id=user.id,
            name=pill_name,
            schedule="custom",
            time=time_obj
        )
        
        session.add(new_medication)
        await session.commit()

        # Получаем ID созданного лекарства
        medication_id = new_medication.id
        
        # Создаем запись в чеклисте на сегодня
        from database.models import Checklist
        from datetime import date
        
        today = date.today()
        
        # Проверяем, не существует ли уже такая запись
        checklist_query = select(Checklist).where(
            Checklist.user_id == user.id,
            Checklist.medication_id == medication_id,
            Checklist.date == today
        )
        existing_checklist = (await session.execute(checklist_query)).scalar_one_or_none()
        
        if not existing_checklist:
            # Создаем новую запись в чеклисте
            new_checklist = Checklist(
                user_id=user.id,
                medication_id=medication_id,
                date=today,
                status=False  # Лекарство еще не принято
            )
            session.add(new_checklist)
            await session.commit()

    # Confirm pill addition
    await message.answer(
        get_text("pill_added", language, name=pill_name, time=time_input)
    )
    
    await setup_medication_reminders(bot)
    
    # Clear state
    await state.clear()
    
    log_user_action(user_id, "pill_added", f"{pill_name} at {time_input}")


@router.message(Command("my_pills"))
@router.message(F.text.func(lambda text: text in ["Мои лекарства", "My medications"]))
async def cmd_my_pills(message: types.Message):
    """Handle showing user's medications list"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Get user's medications
        medications_query = select(Medication).where(
            Medication.user_id == user.id
        ).order_by(Medication.schedule, Medication.time)
        
        medications = (await session.execute(medications_query)).scalars().all()
        
        if not medications:
            await message.answer(get_text("no_medications", user.language, 
                                         default="You haven't added any medications yet."))
            return
        
        # Format the medications list
        message_text = get_text("your_medications", user.language, 
                               default="Your medications:") + "\n\n"
        
        # Group medications by schedule
        morning_meds = []
        day_meds = []
        evening_meds = []
        custom_meds = []
        
        for med in medications:
            time_str = med.time.strftime("%H:%M")
            med_info = f"{med.name} - {time_str}"
            
            if med.schedule == "morning":
                morning_meds.append((med.id, med_info))
            elif med.schedule == "day":
                day_meds.append((med.id, med_info))
            elif med.schedule == "evening":
                evening_meds.append((med.id, med_info))
            else:  # custom
                custom_meds.append((med.id, med_info))
        
        # Add morning section
        if morning_meds:
            message_text += get_text("morning_pills", user.language) + "\n"
            for med_id, med_info in morning_meds:
                message_text += f"{med_info}\n"
            message_text += "\n"
        
        # Add day section
        if day_meds:
            message_text += get_text("day_pills", user.language) + "\n"
            for med_id, med_info in day_meds:
                message_text += f"{med_info}\n"
            message_text += "\n"
        
        # Add evening section
        if evening_meds:
            message_text += get_text("evening_pills", user.language) + "\n"
            for med_id, med_info in evening_meds:
                message_text += f"{med_info}\n"
            message_text += "\n"
        
        # Add custom section
        if custom_meds:
            message_text += get_text("custom_pills", user.language, 
                                    default="🕒 Custom time:") + "\n"
            for med_id, med_info in custom_meds:
                message_text += f"{med_info}\n"
        
        # Send the medications list
        await message.answer(message_text)
        
        # Create keyboard for medication management
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text=get_text("delete_medication", user.language, default="Delete medication"), 
                callback_data="manage_pills:delete"
            )]
        ])
        
        await message.answer(
            get_text("manage_medications", user.language, default="What would you like to do?"),
            reply_markup=keyboard
        )
        
        log_user_action(user_id, "viewed_medications_list")

@router.callback_query(F.data == "manage_pills:delete")
async def manage_pills_delete(callback: types.CallbackQuery):
    """Handle medication deletion selection"""
    user_id = callback.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get user's medications
        medications_query = select(Medication).where(
            Medication.user_id == user.id
        ).order_by(Medication.name)
        
        medications = (await session.execute(medications_query)).scalars().all()
        
        if not medications:
            await callback.answer(get_text("no_medications", user.language, 
                                         default="You haven't added any medications yet."))
            return
        
        # Create keyboard with all medications
        keyboard_buttons = []
        
        for med in medications:
            time_str = med.time.strftime("%H:%M")
            button_text = f"{med.name} - {time_str}"
            keyboard_buttons.append([types.InlineKeyboardButton(
                text=button_text, 
                callback_data=f"delete_pill:{med.id}"
            )])
        
        # Add cancel button
        keyboard_buttons.append([types.InlineKeyboardButton(
            text=get_text("cancel", user.language, default="Cancel"), 
            callback_data="delete_pill:cancel"
        )])
        
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await callback.message.edit_text(
            get_text("select_medication_to_delete", user.language, 
                    default="Select medication to delete:"),
            reply_markup=keyboard
        )
        
        log_user_action(user_id, "medication_deletion_menu")
        await callback.answer()

@router.callback_query(F.data == "delete_pill:cancel")
async def delete_pill_cancel(callback: types.CallbackQuery):
    """Handle cancellation of medication deletion"""
    user_id = callback.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
    
    await callback.message.edit_text(
        get_text("deletion_cancelled", user.language, 
                default="Operation cancelled.")
    )
    
    log_user_action(user_id, "medication_deletion_cancelled")
    await callback.answer()

@router.callback_query(F.data.startswith("delete_pill:"))
async def delete_pill_confirm(callback: types.CallbackQuery):
    """Handle medication deletion confirmation"""
    user_id = callback.from_user.id
    
    # Skip if it's the cancel button
    if callback.data == "delete_pill:cancel":
        return
    
    # Get medication ID
    medication_id = int(callback.data.split(":")[1])
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get the medication
        medication_query = select(Medication).where(
            Medication.id == medication_id,
            Medication.user_id == user.id
        )
        
        medication = (await session.execute(medication_query)).scalar_one_or_none()
        
        if not medication:
            await callback.answer(get_text("medication_not_found", user.language, 
                                         default="Medication not found."))
            return
        
        # Create confirmation keyboard
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=get_text("confirm_delete", user.language, default="Yes, delete"), 
                    callback_data=f"confirm_delete_pill:{medication_id}"
                ),
                types.InlineKeyboardButton(
                    text=get_text("cancel", user.language, default="Cancel"), 
                    callback_data="delete_pill:cancel"
                )
            ]
        ])
        
        await callback.message.edit_text(
            get_text("confirm_delete_medication", user.language, 
                    default="Are you sure you want to delete {name}?", name=medication.name),
            reply_markup=keyboard
        )
        
        log_user_action(user_id, "medication_deletion_confirmation", medication.name)
        await callback.answer()

@router.callback_query(F.data.startswith("confirm_delete_pill:"))
async def confirm_delete_pill(callback: types.CallbackQuery):
    """Handle final medication deletion"""
    user_id = callback.from_user.id
    
    # Get medication ID
    medication_id = int(callback.data.split(":")[1])
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get the medication
        medication_query = select(Medication).where(
            Medication.id == medication_id,
            Medication.user_id == user.id
        )
        
        medication = (await session.execute(medication_query)).scalar_one_or_none()
        
        if not medication:
            await callback.answer(get_text("medication_not_found", user.language, 
                                         default="Medication not found."))
            return
        
        # Store name for the message
        medication_name = medication.name
        print(medication_name)
        # Delete all related checklist items
        from sqlalchemy import delete
        from database.models import Checklist
        
        delete_checklist = delete(Checklist).where(
            Checklist.medication_id == medication_id
        )
        
        await session.execute(delete_checklist)
        
        # Delete the medication
        await session.delete(medication)
        await session.commit()
        
        await callback.message.edit_text(
            get_text("medication_deleted", user.language, name=medication_name)
        )
        
        log_user_action(user_id, "medication_deleted", medication_name)
        await callback.answer()
