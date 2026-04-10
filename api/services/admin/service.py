from api.core.exceptions import NotFoundError
from api.services.admin.repository import AdminRepository
from api.services.admin.schemas import (
    AdminLogListResponse,
    AdminLogResponse,
    AdminStatsResponse,
    AdminUserListResponse,
    AdminUserResponse,
)
from shared.database.models import User


class AdminService:
    def __init__(self, repository: AdminRepository, user: User):
        self._repository = repository
        self._user = user

    async def get_statistics(self) -> AdminStatsResponse:
        total_users = await self._repository.count_total_users()
        active_users = await self._repository.count_active_users()
        avg_pills = await self._repository.get_avg_medications()
        taken_rate = await self._repository.get_taken_rate()
        dau = await self._repository.get_dau()
        new_today = await self._repository.get_new_users_count(1)
        new_week = await self._repository.get_new_users_count(7)
        new_month = await self._repository.get_new_users_count(30)
        weekly_regs = await self._repository.get_weekly_registrations()
        recent_raw = await self._repository.get_recent_users()
        top_meds_raw = await self._repository.get_top_medications()

        from api.services.admin.schemas import (
            RecentUserResponse,
            TopMedicationResponse,
        )

        return AdminStatsResponse(
            total_users=total_users,
            active_users=active_users,
            avg_pills=avg_pills,
            taken_rate=taken_rate,
            dau=dau,
            new_today=new_today,
            new_week=new_week,
            new_month=new_month,
            weekly_registrations=weekly_regs,
            recent_users=[RecentUserResponse(**u) for u in recent_raw],
            top_medications=[TopMedicationResponse(name=n, users=c) for n, c in top_meds_raw],
        )

    async def list_users(self, limit: int = 100, offset: int = 0) -> AdminUserListResponse:
        users, total = await self._repository.find_all_users(limit, offset)
        items = [
            AdminUserResponse(
                id=u.id,
                telegram_id=u.telegram_id,
                language=u.language,
                is_blocked=u.is_blocked,
                created_at=u.created_at,
                last_active=u.last_active,
            )
            for u in users
        ]
        return AdminUserListResponse(users=items, total=total)

    async def ban_user(self, telegram_id: int) -> None:
        target = await self._repository.find_user_by_telegram_id(telegram_id)
        if target is None:
            raise NotFoundError("user_not_found")
        await self._repository.set_user_blocked(target.id, True)
        await self._repository.create_log(
            admin_id=self._user.telegram_id,
            action="ban_user",
            details=f"Banned user with telegram_id {telegram_id}",
        )

    async def unban_user(self, telegram_id: int) -> None:
        target = await self._repository.find_user_by_telegram_id(telegram_id)
        if target is None:
            raise NotFoundError("user_not_found")
        await self._repository.set_user_blocked(target.id, False)
        await self._repository.create_log(
            admin_id=self._user.telegram_id,
            action="unban_user",
            details=f"Unbanned user with telegram_id {telegram_id}",
        )

    async def get_logs(self, limit: int = 50) -> AdminLogListResponse:
        logs = await self._repository.get_logs(limit)
        items = [
            AdminLogResponse(
                id=log.id,
                admin_id=log.admin_id,
                action=log.action,
                details=log.details,
                created_at=log.created_at,
            )
            for log in logs
        ]
        return AdminLogListResponse(logs=items, count=len(items))
