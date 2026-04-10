from datetime import UTC, date, datetime, timedelta

from sqlalchemy import and_, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import AdminLog, Checklist, Medication, User


class AdminRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def count_total_users(self) -> int:
        query = select(func.count()).select_from(User)
        result = await self._session.execute(query)
        return result.scalar() or 0

    async def count_active_users(self, days: int = 7) -> int:
        cutoff = datetime.now(UTC) - timedelta(days=days)
        query = select(func.count()).select_from(User).where(User.last_active >= cutoff)
        result = await self._session.execute(query)
        return result.scalar() or 0

    async def get_avg_medications(self) -> float:
        subquery = (
            select(func.count())
            .select_from(Medication)
            .where(Medication.user_id == User.id)
            .correlate(User)
            .scalar_subquery()
        )
        query = select(func.avg(subquery)).select_from(User)
        result = await self._session.execute(query)
        return round(result.scalar() or 0.0, 2)

    async def get_taken_rate(self) -> float:
        today = date.today()
        total_q = select(func.count()).select_from(Checklist).where(Checklist.date == today)
        taken_q = (
            select(func.count())
            .select_from(Checklist)
            .where(and_(Checklist.date == today, Checklist.status.is_(True)))
        )
        total = (await self._session.execute(total_q)).scalar() or 0
        taken = (await self._session.execute(taken_q)).scalar() or 0
        if total == 0:
            return 0.0
        return round((taken / total) * 100, 1)

    async def get_top_medications(self, limit: int = 5) -> list[tuple[str, int]]:
        query = (
            select(
                Medication.name,
                func.count(func.distinct(Medication.user_id)).label("cnt"),
            )
            .group_by(Medication.name)
            .order_by(desc("cnt"))
            .limit(limit)
        )
        result = await self._session.execute(query)
        return [(row[0], row[1]) for row in result]

    async def get_weekly_registrations(self) -> list[int]:
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        result = []
        for i in range(7):
            day = monday + timedelta(days=i)
            q = select(func.count()).select_from(User).where(func.date(User.created_at) == day)
            count = (await self._session.execute(q)).scalar() or 0
            result.append(count)
        return result

    async def get_recent_users(self, limit: int = 3) -> list[dict]:
        query = select(User).order_by(desc(User.created_at)).limit(limit)
        result = await self._session.execute(query)
        users = list(result.scalars().all())
        items = []
        for u in users:
            meds_q = select(func.count()).select_from(Medication).where(Medication.user_id == u.id)
            meds_count = (await self._session.execute(meds_q)).scalar() or 0

            now = datetime.now(UTC)
            created = u.created_at
            if created and created.tzinfo is None:
                created = created.replace(tzinfo=UTC)
            diff = now - created if created else timedelta()
            if diff.total_seconds() < 60:
                ago = f"{int(diff.total_seconds())}s ago"
            elif diff.total_seconds() < 3600:
                ago = f"{int(diff.total_seconds() // 60)} min ago"
            elif diff.total_seconds() < 86400:
                ago = f"{int(diff.total_seconds() // 3600)}h ago"
            else:
                ago = f"{int(diff.days)}d ago"

            items.append(
                {
                    "id": u.telegram_id,
                    "registered_ago": ago,
                    "meds_count": meds_count,
                }
            )
        return items

    async def get_dau(self) -> int:
        today = date.today()
        q = select(func.count()).select_from(User).where(func.date(User.last_active) == today)
        return (await self._session.execute(q)).scalar() or 0

    async def get_new_users_count(self, days: int) -> int:
        cutoff = datetime.now(UTC) - timedelta(days=days)
        q = select(func.count()).select_from(User).where(User.created_at >= cutoff)
        return (await self._session.execute(q)).scalar() or 0

    async def find_all_users(self, limit: int = 100, offset: int = 0) -> tuple[list[User], int]:
        count_query = select(func.count()).select_from(User)
        total = (await self._session.execute(count_query)).scalar() or 0

        query = select(User).order_by(desc(User.created_at)).limit(limit).offset(offset)
        result = await self._session.execute(query)
        users = list(result.scalars().all())
        return users, total

    async def find_user_by_telegram_id(self, telegram_id: int) -> User | None:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def set_user_blocked(self, user_id: int, blocked: bool) -> None:
        await self._session.execute(
            update(User).where(User.id == user_id).values(is_blocked=blocked)
        )
        await self._session.flush()

    async def create_log(self, admin_id: int, action: str, details: str | None = None) -> AdminLog:
        log = AdminLog(admin_id=admin_id, action=action, details=details)
        self._session.add(log)
        await self._session.flush()
        return log

    async def get_logs(self, limit: int = 50) -> list[AdminLog]:
        query = select(AdminLog).order_by(desc(AdminLog.created_at)).limit(limit)
        result = await self._session.execute(query)
        return list(result.scalars().all())
