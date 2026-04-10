from fastapi import APIRouter, Depends, Query

from api.core.response import ApiResponse
from api.dependencies import get_admin_service
from api.services.admin.schemas import (
    AdminBanRequest,
    AdminLogListResponse,
    AdminStatsResponse,
    AdminUserListResponse,
)
from api.services.admin.service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=ApiResponse[AdminStatsResponse])
async def get_statistics(
    service: AdminService = Depends(get_admin_service),
):
    stats = await service.get_statistics()
    return ApiResponse.ok(stats)


@router.get("/users", response_model=ApiResponse[AdminUserListResponse])
async def list_users(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: AdminService = Depends(get_admin_service),
):
    users = await service.list_users(limit, offset)
    return ApiResponse.ok(users)


@router.post("/ban", response_model=ApiResponse[None])
async def ban_user(
    data: AdminBanRequest,
    service: AdminService = Depends(get_admin_service),
):
    await service.ban_user(data.telegram_id)
    return ApiResponse.ok(None)


@router.post("/unban", response_model=ApiResponse[None])
async def unban_user(
    data: AdminBanRequest,
    service: AdminService = Depends(get_admin_service),
):
    await service.unban_user(data.telegram_id)
    return ApiResponse.ok(None)


@router.get("/logs", response_model=ApiResponse[AdminLogListResponse])
async def get_logs(
    limit: int = Query(50, ge=1, le=500),
    service: AdminService = Depends(get_admin_service),
):
    logs = await service.get_logs(limit)
    return ApiResponse.ok(logs)
