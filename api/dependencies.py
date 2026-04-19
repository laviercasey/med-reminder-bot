from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import api_config
from api.core.exceptions import ForbiddenError, UnauthorizedError
from api.services.auth import jwt_service
from shared.database import db as _db
from shared.database.models import User

if TYPE_CHECKING:
    from api.services.admin.service import AdminService
    from api.services.checklist.service import ChecklistService
    from api.services.medication.service import MedicationService
    from api.services.pubsub.publisher import RedisPublisher
    from api.services.settings.service import SettingsService
    from api.services.user.service import UserService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if _db.async_session_maker is None:
        raise RuntimeError("Database session maker is not configured")
    async with _db.async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    authorization: str | None = Header(default=None),
) -> User:
    if authorization is None or not authorization.strip():
        raise UnauthorizedError("missing_authorization")

    parts = authorization.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        raise UnauthorizedError("invalid_token_scheme")

    token = parts[1].strip()

    try:
        claims = jwt_service.decode_access(token)
    except jwt_service.TokenExpiredError:
        raise UnauthorizedError("token_expired")
    except jwt_service.WrongTokenTypeError:
        raise UnauthorizedError("wrong_token_type")
    except jwt_service.InvalidTokenError:
        raise UnauthorizedError("invalid_token")

    sub = claims.get("sub")
    try:
        telegram_id = int(sub)
    except (TypeError, ValueError):
        raise UnauthorizedError("invalid_token")

    user = (
        await session.execute(select(User).where(User.telegram_id == telegram_id))
    ).scalar_one_or_none()

    if user is None:
        raise UnauthorizedError("user_not_found")

    if user.is_blocked:
        raise ForbiddenError("user_blocked")

    return user


async def require_admin(
    user: User = Depends(get_current_user),
) -> User:
    if user.telegram_id not in api_config.admin_ids:
        raise ForbiddenError("admin_access_required")
    return user


async def get_publisher() -> RedisPublisher:
    from api.services.pubsub.publisher import RedisPublisher
    from shared.redis import get_redis_client

    redis = await get_redis_client()
    return RedisPublisher(redis)


def get_medication_service(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> MedicationService:
    from api.services.medication.repository import MedicationRepository
    from api.services.medication.service import MedicationService

    repository = MedicationRepository(session)
    return MedicationService(repository, user)


def get_checklist_service(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> ChecklistService:
    from api.services.checklist.repository import ChecklistRepository
    from api.services.checklist.service import ChecklistService

    repository = ChecklistRepository(session)
    return ChecklistService(repository, user)


def get_settings_service(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> SettingsService:
    from api.services.settings.repository import SettingsRepository
    from api.services.settings.service import SettingsService

    repository = SettingsRepository(session)
    return SettingsService(repository, user)


def get_user_service(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> UserService:
    from api.services.user.repository import UserRepository
    from api.services.user.service import UserService

    repository = UserRepository(session)
    return UserService(repository, user)


def get_admin_service(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(require_admin),
) -> AdminService:
    from api.services.admin.repository import AdminRepository
    from api.services.admin.service import AdminService
    from api.services.auth.repository import RefreshTokenRepository

    repository = AdminRepository(session)
    refresh_repo = RefreshTokenRepository(session)
    return AdminService(repository, user, refresh_repo=refresh_repo)
