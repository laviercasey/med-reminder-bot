from datetime import datetime, timedelta
from sqlalchemy import select, update
from database.models import User, Payment
from database.db import get_session
from config.config import settings
from utils.logger import log_payment
from aiogram.types import LabeledPrice, PreCheckoutQuery

async def is_premium_active(user: User) -> bool:
    """Check if user has an active premium subscription"""
    if not user.is_premium:
        return False
    
    # Lifetime subscription
    if user.premium_until is None:
        return True
    
    # Subscription with expiration date
    return datetime.utcnow() < user.premium_until

async def get_subscription_invoice(subscription_type: str, user_language: str) -> tuple:
    """Get invoice data for subscription purchase"""
    if subscription_type == "monthly":
        title = "Monthly Premium Subscription" if user_language == "en" else "Месячная премиум-подписка"
        description = "Remove ads and support the app for one month" if user_language == "en" else "Отключение рекламы и поддержка приложения на один месяц"
        price = settings.MONTHLY_PRICE
        duration_days = 30
    elif subscription_type == "yearly":
        title = "Yearly Premium Subscription" if user_language == "en" else "Годовая премиум-подписка"
        description = "Remove ads and support the app for one year" if user_language == "en" else "Отключение рекламы и поддержка приложения на один год"
        price = settings.YEARLY_PRICE
        duration_days = 365
    elif subscription_type == "lifetime":
        title = "Lifetime Premium Subscription" if user_language == "en" else "Бессрочная премиум-подписка"
        description = "Remove ads forever and support the app" if user_language == "en" else "Отключение рекламы навсегда и поддержка приложения"
        price = settings.LIFETIME_PRICE
        duration_days = None
    else:
        raise ValueError(f"Invalid subscription type: {subscription_type}")
    
    prices = [LabeledPrice(label=title, amount=price)]
    
    return title, description, prices, duration_days

async def process_successful_payment(telegram_id: int, subscription_type: str, payment_info, duration_days: int = None):
    """Process successful payment and update user subscription"""
    async with get_session() as session:
        # Get user
        user_query = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return False
        
        # Calculate new subscription end date
        if duration_days is None:  # Lifetime subscription
            new_premium_until = None
        else:
            # If user already has active subscription, extend it
            if user.is_premium and user.premium_until and user.premium_until > datetime.utcnow():
                new_premium_until = user.premium_until + timedelta(days=duration_days)
            else:
                new_premium_until = datetime.utcnow() + timedelta(days=duration_days)
        
        # Update user subscription
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_premium=True, premium_until=new_premium_until)
        )
        
        # Record payment
        amount = payment_info.total_amount
        telegram_payment_id = payment_info.telegram_payment_charge_id
        
        new_payment = Payment(
            user_id=user.id,
            amount=amount,
            subscription_type=subscription_type,
            telegram_payment_id=telegram_payment_id,
            status="completed"
        )
        
        session.add(new_payment)
        await session.commit()
        
        # Log payment
        log_payment(
            user_id=telegram_id,
            amount=amount / 100,  # Convert from kopecks to rubles
            plan=subscription_type,
            status="completed"
        )
        
        return True

async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery) -> bool:
    """Process pre-checkout query and validate payment"""
    # Here you could add additional validation if needed
    return True
    