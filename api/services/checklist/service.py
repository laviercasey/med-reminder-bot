from datetime import date

from api.core.exceptions import NotFoundError
from api.services.checklist.repository import ChecklistRepository
from shared.database.models import Medication, User


class ChecklistService:
    def __init__(self, repository: ChecklistRepository, user: User):
        self._repository = repository
        self._user = user

    async def get_today_checklist(self, target_date: date | None = None) -> list[tuple]:
        if target_date is None:
            target_date = date.today()
        return await self._repository.find_by_user_and_date(self._user.id, target_date)

    async def mark_item(self, checklist_id: int, status: bool) -> None:
        item = await self._repository.find_by_id_and_user(checklist_id, self._user.id)
        if item is None:
            raise NotFoundError("checklist_item_not_found")
        await self._repository.update_status(checklist_id, self._user.id, status)

    async def ensure_daily_checklist(
        self, medications: list[Medication], target_date: date | None = None
    ) -> None:
        if target_date is None:
            target_date = date.today()
        await self._repository.ensure_daily_checklist(self._user.id, medications, target_date)
