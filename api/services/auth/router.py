from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import api_config
from api.core.response import ApiResponse
from api.core.security import TelegramAuthService
from api.dependencies import get_current_user, get_session
from api.services.auth.repository import RefreshTokenRepository
from api.services.auth.schemas import (
    LoginRequest,
    LogoutRequest,
    LogoutResponse,
    RefreshRequest,
    TokenPairResponse,
)
from api.services.auth.service import AuthService
from shared.database.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


def _build_service(session: AsyncSession) -> AuthService:
    telegram_auth = TelegramAuthService(api_config.bot_token)
    refresh_repo = RefreshTokenRepository(session)
    return AuthService(session=session, telegram_auth=telegram_auth, refresh_repo=refresh_repo)


@router.post("/login", response_model=ApiResponse[TokenPairResponse])
async def login(
    body: LoginRequest,
    session: AsyncSession = Depends(get_session),
    user_agent: str | None = Header(default=None, alias="User-Agent"),
):
    service = _build_service(session)
    result = await service.login(init_data=body.init_data, user_agent=user_agent)
    return ApiResponse.ok(result)


@router.post("/refresh", response_model=ApiResponse[TokenPairResponse])
async def refresh(
    body: RefreshRequest,
    session: AsyncSession = Depends(get_session),
    user_agent: str | None = Header(default=None, alias="User-Agent"),
):
    service = _build_service(session)
    result = await service.refresh(refresh_token=body.refresh_token, user_agent=user_agent)
    return ApiResponse.ok(result)


@router.post("/logout", response_model=ApiResponse[LogoutResponse])
async def logout(
    body: LogoutRequest,
    session: AsyncSession = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    service = _build_service(session)
    revoked = await service.logout(refresh_token=body.refresh_token)
    return ApiResponse.ok(LogoutResponse(revoked=revoked))
