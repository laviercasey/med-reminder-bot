from datetime import time

from sqlalchemy import delete as sa_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import Checklist, Medication


class MedicationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_user(self, user_id: int) -> list[Medication]:
        query = (
            select(Medication)
            .where(Medication.user_id == user_id)
            .order_by(Medication.schedule, Medication.time)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def find_by_id(self, medication_id: int) -> Medication | None:
        query = select(Medication).where(Medication.id == medication_id)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def find_by_id_and_user(self, medication_id: int, user_id: int) -> Medication | None:
        query = select(Medication).where(
            Medication.id == medication_id,
            Medication.user_id == user_id,
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: int,
        name: str,
        schedule: str,
        time: time,
    ) -> Medication:
        medication = Medication(
            user_id=user_id,
            name=name,
            schedule=schedule,
            time=time,
        )
        self._session.add(medication)
        await self._session.flush()
        return medication

    async def update(
        self,
        medication: Medication,
        name: str,
        schedule: str,
        time: time,
    ) -> Medication:
        medication.name = name
        medication.schedule = schedule
        medication.time = time
        await self._session.flush()
        return medication

    async def delete(self, medication_id: int) -> None:
        await self._session.execute(
            sa_delete(Checklist).where(Checklist.medication_id == medication_id)
        )
        medication = await self.find_by_id(medication_id)
        if medication:
            await self._session.delete(medication)
            await self._session.flush()
