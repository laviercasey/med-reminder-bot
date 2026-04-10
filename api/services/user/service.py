from api.core.config import api_config
from api.services.user.repository import UserRepository
from api.services.user.schemas import UserProfileResponse
from shared.database.models import User


class UserService:
    def __init__(self, repository: UserRepository, user: User):
        self._repository = repository
        self._user = user

    async def get_profile(self) -> UserProfileResponse:
        await self._repository.update_last_active(self._user.id)
        medications_count = await self._repository.count_medications(self._user.id)
        return UserProfileResponse(
            id=self._user.id,
            telegram_id=self._user.telegram_id,
            language=self._user.language,
            is_admin=self._user.telegram_id in api_config.admin_ids,
            created_at=self._user.created_at,
            last_active=self._user.last_active,
            medications_count=medications_count,
        )
