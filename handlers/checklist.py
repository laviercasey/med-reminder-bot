from aiogram import Router, F, types
from aiogram.filters import Command
from sqlalchemy import select, update
from database.models import User, Medication, Checklist
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_checklist_keyboard
from utils.logger import log_user_action
from datetime import datetime, time
from services.payments import is_premium_active

router = Router()

@router.message(Command("today"))
@router.message(F.text.func(lambda text: text in ["Лекарства на сегодня", "Today's medications"]))
async def cmd_today_checklist(message: types.Message):
    """Handle showing today's medication checklist"""
    user_id = message.from_user.id
    today = datetime.now().date()
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Get user's checklist items for today
        checklist_query = select(Checklist, Medication).join(
            Medication, Checklist.medication_id == Medication.id
        ).where(
            Checklist.user_id == user.id,
            Checklist.date == today
        ).order_by(Medication.time)
        
        result = await session.execute(checklist_query)
        checklist_items = result.all()
        
        if not checklist_items:
            # Если чеклист пуст, попробуем создать его
            medications_query = select(Medication).where(Medication.user_id == user.id)
            medications = (await session.execute(medications_query)).scalars().all()
            
            if medications:
                # Есть лекарства, но нет чеклиста - создаем его
                for medication in medications:
                    new_checklist = Checklist(
                        user_id=user.id,
                        medication_id=medication.id,
                        date=today,
                        status=False
                    )
                    session.add(new_checklist)
                await session.commit()
                
                # Повторно запрашиваем чеклист
                result = await session.execute(checklist_query)
                checklist_items = result.all()
            
            if not checklist_items:
                await message.answer(get_text("no_pills_today", user.language))
                return
        
        # Group medications by schedule (morning, day, evening)
        morning_items = []
        day_items = []
        evening_items = []
        
        for checklist, medication in checklist_items:
            item_time = medication.time
            item_text = get_text(
                "pill_item", 
                user.language,
                name=medication.name,
                time=item_time.strftime("%H:%M")
            )
            
            if medication.schedule == "morning" or (item_time.hour >= 5 and item_time.hour < 12):
                morning_items.append((checklist, item_text))
            elif medication.schedule == "day" or (item_time.hour >= 12 and item_time.hour < 18):
                day_items.append((checklist, item_text))
            else:
                evening_items.append((checklist, item_text))
        
        # Format the checklist message
        today_formatted = today.strftime("%d.%m.%Y")
        message_text = get_text("today_checklist", user.language, date=today_formatted) + "\n\n"
        
        # Add morning section
        if morning_items:
            message_text += get_text("morning_pills", user.language) + "\n"
            for checklist, item_text in morning_items:
                status = "✅ " if checklist.status else ""
                message_text += f"{status}{item_text}\n"
            message_text += "\n"
        
        # Add day section
        if day_items:
            message_text += get_text("day_pills", user.language) + "\n"
            for checklist, item_text in day_items:
                status = "✅ " if checklist.status else ""
                message_text += f"{status}{item_text}\n"
            message_text += "\n"
        
        # Add evening section
        if evening_items:
            message_text += get_text("evening_pills", user.language) + "\n"
            for checklist, item_text in evening_items:
                status = "✅ " if checklist.status else ""
                message_text += f"{status}{item_text}\n"
        
        # Add ad for non-premium users
        is_premium = await is_premium_active(user)
        if not is_premium:
            message_text += "\n" + get_text("ad_banner", user.language)
        
        # Send the checklist
        await message.answer(message_text)
        
        # Send buttons for items that haven't been marked as taken
        for checklist, medication in checklist_items:
            if not checklist.status:
                pill_name = medication.name
                pill_time = medication.time.strftime("%H:%M")
                
                await message.answer(
                    f"{pill_name} - {pill_time}",
                    reply_markup=get_checklist_keyboard(checklist.id, user.language)
                )
        
        log_user_action(user_id, "viewed_today_checklist")

@router.callback_query(F.data.startswith("mark_taken:"))
async def process_mark_as_taken(callback: types.CallbackQuery):
    """Process marking medication as taken"""
    user_id = callback.from_user.id
    checklist_id = int(callback.data.split(":")[1])
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get checklist item
        checklist_query = select(Checklist, Medication).join(
            Medication, Checklist.medication_id == Medication.id
        ).where(
            Checklist.id == checklist_id,
            Checklist.user_id == user.id
        )
        
        result = await session.execute(checklist_query)
        checklist_data = result.first()
        
        if not checklist_data:
            await callback.answer()
            return
        
        checklist, medication = checklist_data
        
        # Mark as taken
        await session.execute(
            update(Checklist)
            .where(Checklist.id == checklist_id)
            .values(status=True)
        )
        
        await session.commit()
        
        # Update message
        await callback.message.edit_text(
            f"✅ {medication.name} - {medication.time.strftime('%H:%M')}"
        )
        
        await callback.answer(
            get_text("marked_as_taken", user.language, name=medication.name)
        )
        
        log_user_action(user_id, "marked_pill_taken", medication.name)


@router.message(Command("update_checklist"))
async def cmd_update_checklist(message: types.Message):
    """Manually update today's checklist"""
    user_id = message.from_user.id
    today = datetime.now().date()
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Get user's medications
        medications_query = select(Medication).where(Medication.user_id == user.id)
        medications = (await session.execute(medications_query)).scalars().all()
        
        if not medications:
            await message.answer(get_text("no_pills_today", user.language))
            return
        
        # Count of new entries
        new_entries = 0
        
        # Create checklist items for each medication
        for medication in medications:
            # Check if checklist item already exists
            checklist_query = select(Checklist).where(
                Checklist.user_id == user.id,
                Checklist.medication_id == medication.id,
                Checklist.date == today
            )
            
            existing_checklist = (await session.execute(checklist_query)).scalar_one_or_none()
            
            if not existing_checklist:
                # Create new checklist item
                new_checklist = Checklist(
                    user_id=user.id,
                    medication_id=medication.id,
                    date=today,
                    status=False
                )
                session.add(new_checklist)
                new_entries += 1
        
        await session.commit()
        
        if new_entries > 0:
            await message.answer(f"Чеклист обновлен. Добавлено {new_entries} новых записей.")
        else:
            await message.answer("Чеклист уже актуален, новых записей не добавлено.")
        
        # Перенаправляем на просмотр чеклиста
        await cmd_today_checklist(message)
