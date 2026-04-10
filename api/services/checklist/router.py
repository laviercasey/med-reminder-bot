from datetime import date

from fastapi import APIRouter, Depends, Query

from api.core.response import ApiResponse
from api.dependencies import get_checklist_service, get_medication_service
from api.services.checklist.schemas import (
    ChecklistItemResponse,
    ChecklistMarkRequest,
    ChecklistResponse,
)
from api.services.checklist.service import ChecklistService
from api.services.medication.service import MedicationService

router = APIRouter(prefix="/checklist", tags=["checklist"])


@router.get("", response_model=ApiResponse[ChecklistResponse])
async def get_today_checklist(
    target_date: date | None = Query(None, alias="date"),
    checklist_service: ChecklistService = Depends(get_checklist_service),
    medication_service: MedicationService = Depends(get_medication_service),
):
    effective_date = target_date or date.today()
    medications = await medication_service.list_medications()

    if medications:
        await checklist_service.ensure_daily_checklist(medications, effective_date)

    items_raw = await checklist_service.get_today_checklist(effective_date)

    items = [
        ChecklistItemResponse(
            id=checklist.id,
            medication_id=medication.id,
            medication_name=medication.name,
            medication_time=medication.time.strftime("%H:%M"),
            schedule=medication.schedule,
            date=checklist.date,
            status=checklist.status,
            updated_at=checklist.updated_at,
        )
        for checklist, medication in items_raw
    ]

    taken_count = sum(1 for item in items if item.status)

    return ApiResponse.ok(
        ChecklistResponse(
            items=items,
            date=effective_date,
            total=len(items),
            taken=taken_count,
        )
    )


@router.patch("/{checklist_id}", response_model=ApiResponse[None])
async def mark_checklist_item(
    checklist_id: int,
    body: ChecklistMarkRequest,
    service: ChecklistService = Depends(get_checklist_service),
):
    await service.mark_item(checklist_id, body.status)
    return ApiResponse.ok(None)
