from api.core.exceptions import NotFoundError
from api.services.medication.repository import MedicationRepository
from api.services.medication.schemas import MedicationCreate, MedicationUpdate
from shared.database.models import Medication, User


class MedicationService:
    def __init__(self, repository: MedicationRepository, user: User):
        self._repository = repository
        self._user = user

    async def list_medications(self) -> list[Medication]:
        return await self._repository.find_by_user(self._user.id)

    async def get_medication(self, medication_id: int) -> Medication:
        medication = await self._repository.find_by_id_and_user(medication_id, self._user.id)
        if medication is None:
            raise NotFoundError("medication_not_found")
        return medication

    async def add_medication(self, data: MedicationCreate) -> Medication:
        return await self._repository.create(
            user_id=self._user.id,
            name=data.name,
            schedule=data.schedule,
            time=data.time,
        )

    async def update_medication(self, medication_id: int, data: MedicationUpdate) -> Medication:
        medication = await self._repository.find_by_id_and_user(medication_id, self._user.id)
        if medication is None:
            raise NotFoundError("medication_not_found")
        return await self._repository.update(
            medication=medication,
            name=data.name,
            schedule=data.schedule,
            time=data.time,
        )

    async def delete_medication(self, medication_id: int) -> None:
        medication = await self._repository.find_by_id_and_user(medication_id, self._user.id)
        if medication is None:
            raise NotFoundError("medication_not_found")
        await self._repository.delete(medication_id)
