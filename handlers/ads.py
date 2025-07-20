from aiogram import Router, F, types
from aiogram.filters import Command
from sqlalchemy import select
from database.models import User
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_subscription_keyboard
from utils.logger import log_user_action
from services.payments import is_premium_active, get_subscription_invoice
from config.config import settings
from datetime import datetime

router = Router()

@router.message(Command("subscription"))
@router.message(F.text.func(lambda text: text in ["Подписка", "Subscription"]))
async def cmd_subscription(message: types.Message):
    """Handle subscription command"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Check subscription status
        is_premium = await is_premium_active(user)
        
        # Create message based on subscription status
        message_text = get_text("subscription_info", user.language) + "\n\n"
        
        if not is_premium:
            message_text += get_text("free_plan", user.language)
        elif user.premium_until is None:
            message_text += get_text("lifetime_plan", user.language)
        else:
            expiry_date = user.premium_until.strftime("%d.%m.%Y")
            message_text += get_text("premium_plan", user.language, date=expiry_date)
        
        # Add subscription options
        if not (is_premium and user.premium_until is None):  # Don't show options for lifetime subscribers
            message_text += "\n\n" + get_text("subscription_plans", user.language)
            
            await message.answer(
                message_text,
                reply_markup=get_subscription_keyboard(user.language)
            )
        else:
            await message.answer(message_text)
        
        log_user_action(user_id, "viewed_subscription")

@router.callback_query(F.data.startswith("subscribe:"))
async def process_subscription_selection(callback: types.CallbackQuery):
    """Process subscription plan selection"""
    user_id = callback.from_user.id
    plan = callback.data.split(":")[1]  # "subscribe:monthly" -> "monthly"
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get invoice details
        title, description, prices, duration_days = await get_subscription_invoice(plan, user.language)
        
        # Create invoice
        await callback.bot.send_invoice(
            chat_id=user_id,
            title=title,
            description=description,
            payload=f"subscription:{plan}:{duration_days}",
            provider_token=settings.PAYMENT_PROVIDER_TOKEN,
            currency="RUB",
            prices=prices
        )
        
        log_user_action(user_id, "selected_subscription_plan", plan)
        await callback.answer()

@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    """Handle pre-checkout queries"""
    from services.payments import process_pre_checkout
    
    # Validate pre-checkout
    is_valid = await process_pre_checkout(pre_checkout_query)
    
    if is_valid:
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(ok=False, error_message="Payment processing error. Please try again later.")

@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    """Handle successful payment"""
    from services.payments import process_successful_payment
    
    user_id = message.from_user.id
    payment_info = message.successful_payment
    
    # Parse payload
    payload_parts = payment_info.invoice_payload.split(":")
    if len(payload_parts) != 3:
        return
    
    _, subscription_type, duration_days = payload_parts
    duration_days = None if duration_days == "None" else int(duration_days)
    
    # Process payment
    success = await process_successful_payment(
        telegram_id=user_id,
        subscription_type=subscription_type,
        payment_info=payment_info,
        duration_days=duration_days
    )
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return
        
        language = user.language
    
    # Send confirmation
    if success:
        await message.answer(get_text("payment_success", language))
    else:
        await message.answer(get_text("payment_failed", language))
