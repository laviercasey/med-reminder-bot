from fastapi import APIRouter, Depends

from api.core.response import ApiResponse
from api.dependencies import get_user_service
from api.services.user.schemas import UserProfileResponse
from api.services.user.service import UserService

router = APIRouter(prefix="/me", tags=["user"])


@router.get("", response_model=ApiResponse[UserProfileResponse])
async def get_profile(
    service: UserService = Depends(get_user_service),
):
    profile = await service.get_profile()
    return ApiResponse.ok(profile)
