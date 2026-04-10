from fastapi import APIRouter, Depends

from api.core.response import ApiResponse
from api.dependencies import get_settings_service
from api.services.settings.schemas import SettingsResponse, SettingsUpdateRequest
from api.services.settings.service import SettingsService

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=ApiResponse[SettingsResponse])
async def get_settings(
    service: SettingsService = Depends(get_settings_service),
):
    settings = await service.get_settings()
    return ApiResponse.ok(settings)


@router.patch("", response_model=ApiResponse[SettingsResponse])
async def update_settings(
    data: SettingsUpdateRequest,
    service: SettingsService = Depends(get_settings_service),
):
    settings = await service.update_settings(data)
    return ApiResponse.ok(settings)
