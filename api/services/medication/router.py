from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.response import ApiResponse
from api.dependencies import get_current_user, get_medication_service, get_publisher, get_session
from api.services.medication.schemas import (
    MedicationCreate,
    MedicationListResponse,
    MedicationResponse,
    MedicationUpdate,
)
from api.services.medication.service import MedicationService
from api.services.pubsub.publisher import RedisPublisher
from shared.database.models import Checklist, User

router = APIRouter(prefix="/medications", tags=["medications"])


@router.get("", response_model=ApiResponse[MedicationListResponse])
async def list_medications(
    service: MedicationService = Depends(get_medication_service),
):
    medications = await service.list_medications()
    items = [
        MedicationResponse(
            id=m.id,
            name=m.name,
            schedule=m.schedule,
            time=m.time.strftime("%H:%M"),
            created_at=m.created_at,
        )
        for m in medications
    ]
    return ApiResponse.ok(MedicationListResponse(medications=items, count=len(items)))


@router.get("/{medication_id}", response_model=ApiResponse[MedicationResponse])
async def get_medication(
    medication_id: int,
    service: MedicationService = Depends(get_medication_service),
):
    medication = await service.get_medication(medication_id)
    return ApiResponse.ok(
        MedicationResponse(
            id=medication.id,
            name=medication.name,
            schedule=medication.schedule,
            time=medication.time.strftime("%H:%M"),
            created_at=medication.created_at,
        )
    )


@router.post("", response_model=ApiResponse[MedicationResponse], status_code=201)
async def create_medication(
    data: MedicationCreate,
    service: MedicationService = Depends(get_medication_service),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
    publisher: RedisPublisher = Depends(get_publisher),
):
    medication = await service.add_medication(data)

    today = date.today()
    existing = await session.execute(
        select(Checklist).where(
            Checklist.user_id == user.id,
            Checklist.medication_id == medication.id,
            Checklist.date == today,
        )
    )
    if existing.scalar_one_or_none() is None:
        session.add(
            Checklist(
                user_id=user.id,
                medication_id=medication.id,
                date=today,
                status=False,
            )
        )

    await publisher.publish_medication_created(user.id, medication.id)

    return ApiResponse.ok(
        MedicationResponse(
            id=medication.id,
            name=medication.name,
            schedule=medication.schedule,
            time=medication.time.strftime("%H:%M"),
            created_at=medication.created_at,
        )
    )


@router.put("/{medication_id}", response_model=ApiResponse[MedicationResponse])
async def update_medication(
    medication_id: int,
    data: MedicationUpdate,
    service: MedicationService = Depends(get_medication_service),
    user: User = Depends(get_current_user),
    publisher: RedisPublisher = Depends(get_publisher),
):
    medication = await service.update_medication(medication_id, data)

    await publisher.publish_medication_updated(user.id, medication.id)

    return ApiResponse.ok(
        MedicationResponse(
            id=medication.id,
            name=medication.name,
            schedule=medication.schedule,
            time=medication.time.strftime("%H:%M"),
            created_at=medication.created_at,
        )
    )


@router.delete("/{medication_id}", response_model=ApiResponse[None])
async def delete_medication(
    medication_id: int,
    service: MedicationService = Depends(get_medication_service),
    user: User = Depends(get_current_user),
    publisher: RedisPublisher = Depends(get_publisher),
):
    await service.delete_medication(medication_id)

    await publisher.publish_medication_deleted(user.id, medication_id)

    return ApiResponse.ok(None)
