from datetime import datetime, timedelta
from sqlalchemy import select, func, update, desc
from database.models import User, Medication, Checklist, Payment, AdminLog
from database.db import get_session
from utils.logger import log_admin_action

async def get_admin_statistics() -> dict:
    """Get statistics for admin panel"""
    async with get_session() as session:
        # Total users count
        total_users_query = select(func.count()).select_from(User)
        total_users = (await session.execute(total_users_query)).scalar()
        
        # Active users in last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_users_query = select(func.count()).select_from(User).where(
            User.last_active >= seven_days_ago
        )
        active_users = (await session.execute(active_users_query)).scalar()
        
        # Premium users count
        premium_users_query = select(func.count()).select_from(User).where(
            User.is_premium == True
        )
        premium_users = (await session.execute(premium_users_query)).scalar()
        
        # Average medications per user
        avg_pills_query = select(func.avg(
            select(func.count())
            .select_from(Medication)
            .where(Medication.user_id == User.id)
            .correlate(User)
            .scalar_subquery()
        )).select_from(User)
        avg_pills = (await session.execute(avg_pills_query)).scalar() or 0
        avg_pills = round(avg_pills, 2)
        
        # Monthly income (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        income_query = select(func.sum(Payment.amount)).where(
            Payment.created_at >= thirty_days_ago,
            Payment.status == "completed"
        )
        monthly_income = (await session.execute(income_query)).scalar() or 0
        monthly_income = monthly_income / 100  # Convert from kopecks to rubles
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "premium_users": premium_users,
            "avg_pills": avg_pills,
            "monthly_income": monthly_income
        }

async def ban_user(admin_id: int, user_telegram_id: int) -> bool:
    """Ban a user"""
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_telegram_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return False
        
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_blocked=True)
        )
        
        # Log admin action
        admin_log = AdminLog(
            admin_id=admin_id,
            action="ban_user",
            details=f"Banned user with telegram_id {user_telegram_id}"
        )
        session.add(admin_log)
        
        await session.commit()
        
        log_admin_action(admin_id, "ban_user", user_telegram_id)
        return True

async def unban_user(admin_id: int, user_telegram_id: int) -> bool:
    """Unban a user"""
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_telegram_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return False
        
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_blocked=False)
        )
        
        # Log admin action
        admin_log = AdminLog(
            admin_id=admin_id,
            action="unban_user",
            details=f"Unbanned user with telegram_id {user_telegram_id}"
        )
        session.add(admin_log)
        
        await session.commit()
        
        log_admin_action(admin_id, "unban_user", user_telegram_id)
        return True

async def extend_subscription(admin_id: int, user_telegram_id: int, days: int) -> bool:
    """Extend user subscription"""
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_telegram_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return False
        
        # Calculate new premium_until date
        if user.is_premium and user.premium_until and user.premium_until > datetime.utcnow():
            new_premium_until = user.premium_until + timedelta(days=days)
        else:
            new_premium_until = datetime.utcnow() + timedelta(days=days)
        
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_premium=True, premium_until=new_premium_until)
        )
        
        # Log admin action
        admin_log = AdminLog(
            admin_id=admin_id,
            action="extend_subscription",
            details=f"Extended subscription for user {user_telegram_id} by {days} days"
        )
        session.add(admin_log)
        
        await session.commit()
        
        log_admin_action(admin_id, "extend_subscription", user_telegram_id)
        return True

async def get_admin_logs(limit: int = 50) -> list:
    """Get recent admin logs"""
    async with get_session() as session:
        logs_query = select(AdminLog).order_by(desc(AdminLog.created_at)).limit(limit)
        logs = (await session.execute(logs_query)).scalars().all()
        return logs

async def export_users_csv() -> str:
    """Export users data to CSV"""
    async with get_session() as session:
        users_query = select(User)
        users = (await session.execute(users_query)).scalars().all()
        
        csv_data = "id,telegram_id,language,is_premium,premium_until,is_blocked,created_at,last_active\n"
        
        for user in users:
            premium_until = user.premium_until.strftime("%Y-%m-%d %H:%M:%S") if user.premium_until else "N/A"
            created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
            last_active = user.last_active.strftime("%Y-%m-%d %H:%M:%S")
            
            csv_data += f"{user.id},{user.telegram_id},{user.language},{user.is_premium},{premium_until},"
            csv_data += f"{user.is_blocked},{created_at},{last_active}\n"
        
        return csv_data
