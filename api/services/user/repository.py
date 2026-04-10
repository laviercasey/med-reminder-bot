from datetime import UTC, datetime

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import Medication, User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def count_medications(self, user_id: int) -> int:
        query = select(func.count()).select_from(Medication).where(Medication.user_id == user_id)
        result = await self._session.execute(query)
        return result.scalar() or 0

    async def update_last_active(self, user_id: int) -> None:
        await self._session.execute(
            update(User).where(User.id == user_id).values(last_active=datetime.now(UTC))
        )
        await self._session.flush()
