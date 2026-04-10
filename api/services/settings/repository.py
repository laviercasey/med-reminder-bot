from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import User, UserSettings


class SettingsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_user(self, user_id: int) -> UserSettings | None:
        query = select(UserSettings).where(UserSettings.user_id == user_id)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def create_default(self, user_id: int) -> UserSettings:
        user_settings = UserSettings(
            user_id=user_id,
            reminders_enabled=True,
            reminder_repeat_minutes=30,
        )
        self._session.add(user_settings)
        await self._session.flush()
        return user_settings

    async def get_or_create(self, user_id: int) -> UserSettings:
        existing = await self.find_by_user(user_id)
        if existing is not None:
            return existing
        return await self.create_default(user_id)

    async def update_settings(
        self,
        user_id: int,
        reminders_enabled: bool | None = None,
        reminder_repeat_minutes: int | None = None,
    ) -> UserSettings:
        settings = await self.get_or_create(user_id)
        if reminders_enabled is not None:
            settings.reminders_enabled = reminders_enabled
        if reminder_repeat_minutes is not None:
            settings.reminder_repeat_minutes = reminder_repeat_minutes
        await self._session.flush()
        return settings

    async def update_user_language(self, user_id: int, language: str) -> None:
        await self._session.execute(
            update(User).where(User.id == user_id).values(language=language)
        )
        await self._session.flush()
