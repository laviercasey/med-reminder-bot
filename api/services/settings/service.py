from api.services.settings.repository import SettingsRepository
from api.services.settings.schemas import SettingsResponse, SettingsUpdateRequest
from shared.database.models import User


class SettingsService:
    def __init__(self, repository: SettingsRepository, user: User):
        self._repository = repository
        self._user = user

    async def get_settings(self) -> SettingsResponse:
        user_settings = await self._repository.get_or_create(self._user.id)
        return SettingsResponse(
            reminders_enabled=user_settings.reminders_enabled,
            reminder_repeat_minutes=user_settings.reminder_repeat_minutes,
            language=self._user.language,
            created_at=user_settings.created_at,
            updated_at=user_settings.updated_at,
        )

    async def update_settings(self, data: SettingsUpdateRequest) -> SettingsResponse:
        if data.language is not None:
            await self._repository.update_user_language(self._user.id, data.language)
        user_settings = await self._repository.update_settings(
            user_id=self._user.id,
            reminders_enabled=data.reminders_enabled,
            reminder_repeat_minutes=data.reminder_repeat_minutes,
        )

        language = data.language if data.language is not None else self._user.language

        return SettingsResponse(
            reminders_enabled=user_settings.reminders_enabled,
            reminder_repeat_minutes=user_settings.reminder_repeat_minutes,
            language=language,
            created_at=user_settings.created_at,
            updated_at=user_settings.updated_at,
        )
