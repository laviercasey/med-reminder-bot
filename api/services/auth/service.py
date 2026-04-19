from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import api_config
from api.core.exceptions import ForbiddenError, UnauthorizedError
from api.core.security import TelegramAuthService
from api.services.auth import jwt_service
from api.services.auth.repository import RefreshTokenRepository
from api.services.auth.schemas import TokenPairResponse
from shared.database.models import User


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        telegram_auth: TelegramAuthService,
        refresh_repo: RefreshTokenRepository,
    ):
        self._session = session
        self._telegram_auth = telegram_auth
        self._refresh_repo = refresh_repo

    async def login(
        self,
        init_data: str,
        user_agent: str | None = None,
    ) -> TokenPairResponse:
        tg_data = self._telegram_auth.validate(init_data, max_age=api_config.max_auth_age)
        telegram_id = tg_data.get("id")
        if telegram_id is None:
            raise UnauthorizedError("invalid_telegram_id")

        user = await self._upsert_user(telegram_id, tg_data.get("language_code", "en"))

        if user.is_blocked:
            raise ForbiddenError("user_blocked")

        return await self._issue_pair(user, user_agent)

    async def refresh(
        self,
        refresh_token: str,
        user_agent: str | None = None,
    ) -> TokenPairResponse:
        token_hash = jwt_service.hash_refresh(refresh_token)
        row = await self._refresh_repo.find_by_hash(token_hash)
        if row is None:
            raise UnauthorizedError("invalid_refresh_token")

        if row.revoked_at is not None:
            await self._refresh_repo.revoke_all_for_user(row.user_id)
            raise UnauthorizedError("refresh_token_reused")

        expires_at = row.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at <= datetime.now(UTC):
            raise UnauthorizedError("refresh_token_expired")

        user = (
            await self._session.execute(select(User).where(User.id == row.user_id))
        ).scalar_one_or_none()
        if user is None:
            raise UnauthorizedError("user_not_found")

        if user.is_blocked:
            await self._refresh_repo.revoke_all_for_user(user.id)
            raise ForbiddenError("user_blocked")

        new_raw = jwt_service.generate_refresh_token()
        new_hash = jwt_service.hash_refresh(new_raw)
        new_expires = datetime.now(UTC) + timedelta(seconds=api_config.jwt_refresh_ttl)

        await self._refresh_repo.create(
            user_id=user.id,
            token_hash=new_hash,
            expires_at=new_expires,
            user_agent=user_agent,
        )
        await self._refresh_repo.revoke(row, replaced_by=new_hash)

        access_token, access_expires_at = jwt_service.issue_access(user)
        return TokenPairResponse(
            access_token=access_token,
            refresh_token=new_raw,
            token_type="Bearer",
            expires_in=api_config.jwt_access_ttl,
            expires_at=access_expires_at,
            refresh_expires_at=int(new_expires.timestamp()),
        )

    async def logout(self, refresh_token: str) -> bool:
        token_hash = jwt_service.hash_refresh(refresh_token)
        row = await self._refresh_repo.find_by_hash(token_hash)
        if row is None or row.revoked_at is not None:
            return False
        await self._refresh_repo.revoke(row)
        return True

    async def _upsert_user(self, telegram_id: int, language_code: str) -> User:
        existing = (
            await self._session.execute(select(User).where(User.telegram_id == telegram_id))
        ).scalar_one_or_none()

        now = datetime.now(UTC)
        language = (language_code or "en")[:2]

        if existing is None:
            user = User(
                telegram_id=telegram_id,
                language=language,
                is_blocked=False,
                created_at=now,
                last_active=now,
            )
            self._session.add(user)
            await self._session.flush()
            return user

        existing.language = language
        existing.last_active = now
        await self._session.flush()
        return existing

    async def _issue_pair(self, user: User, user_agent: str | None) -> TokenPairResponse:
        raw_refresh = jwt_service.generate_refresh_token()
        token_hash = jwt_service.hash_refresh(raw_refresh)
        refresh_expires = datetime.now(UTC) + timedelta(seconds=api_config.jwt_refresh_ttl)

        await self._refresh_repo.create(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=refresh_expires,
            user_agent=user_agent,
        )

        access_token, access_expires_at = jwt_service.issue_access(user)
        return TokenPairResponse(
            access_token=access_token,
            refresh_token=raw_refresh,
            token_type="Bearer",
            expires_in=api_config.jwt_access_ttl,
            expires_at=access_expires_at,
            refresh_expires_at=int(refresh_expires.timestamp()),
        )
