import time
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.exceptions import ForbiddenError, UnauthorizedError
from api.core.security import TelegramAuthService
from api.services.auth import jwt_service
from api.services.auth.repository import RefreshTokenRepository
from api.services.auth.service import AuthService
from shared.database.models import RefreshToken, User
from tests.conftest import (
    TEST_BOT_TOKEN,
    TEST_TELEGRAM_ID,
    build_init_data,
)


@pytest_asyncio.fixture
async def auth_service(test_session: AsyncSession) -> AuthService:
    telegram_auth = TelegramAuthService(TEST_BOT_TOKEN)
    repo = RefreshTokenRepository(test_session)
    return AuthService(session=test_session, telegram_auth=telegram_auth, refresh_repo=repo)


class TestLogin:
    async def test_with_valid_init_data_upserts_user_and_returns_token_pair(
        self, auth_service, test_session
    ):
        init_data = build_init_data(bot_token=TEST_BOT_TOKEN, telegram_id=TEST_TELEGRAM_ID)
        result = await auth_service.login(init_data=init_data, user_agent="ua/1.0")

        assert result.access_token
        assert result.refresh_token
        assert result.expires_in == jwt_service.api_config.jwt_access_ttl
        assert result.expires_at > int(time.time())

        users = (await test_session.execute(select(User))).scalars().all()
        assert len(users) == 1
        assert users[0].telegram_id == TEST_TELEGRAM_ID

        rows = (await test_session.execute(select(RefreshToken))).scalars().all()
        assert len(rows) == 1
        assert rows[0].token_hash == jwt_service.hash_refresh(result.refresh_token)
        assert rows[0].user_agent == "ua/1.0"

    async def test_existing_user_updates_last_active_and_language(
        self, auth_service, test_session
    ):
        existing = User(telegram_id=TEST_TELEGRAM_ID, language="en", is_blocked=False)
        test_session.add(existing)
        await test_session.commit()

        init_data = build_init_data(
            bot_token=TEST_BOT_TOKEN,
            telegram_id=TEST_TELEGRAM_ID,
            language_code="ru",
        )
        await auth_service.login(init_data=init_data)

        await test_session.refresh(existing)
        assert existing.language == "ru"

    async def test_raises_on_invalid_hmac(self, auth_service):
        init_data = build_init_data(bot_token=TEST_BOT_TOKEN, telegram_id=TEST_TELEGRAM_ID)
        tampered = init_data.replace(init_data.split("hash=")[1][:10], "0000000000")
        with pytest.raises(UnauthorizedError, match="invalid_hash"):
            await auth_service.login(init_data=tampered)

    async def test_raises_on_expired_init_data(self, auth_service):
        expired = int(time.time()) - 200000
        init_data = build_init_data(
            bot_token=TEST_BOT_TOKEN, telegram_id=TEST_TELEGRAM_ID, auth_date=expired
        )
        with pytest.raises(UnauthorizedError, match="auth_data_expired"):
            await auth_service.login(init_data=init_data)

    async def test_raises_on_blocked_user(self, auth_service, test_session):
        existing = User(telegram_id=TEST_TELEGRAM_ID, language="en", is_blocked=True)
        test_session.add(existing)
        await test_session.commit()

        init_data = build_init_data(bot_token=TEST_BOT_TOKEN, telegram_id=TEST_TELEGRAM_ID)
        with pytest.raises(ForbiddenError, match="user_blocked"):
            await auth_service.login(init_data=init_data)


class TestRefresh:
    async def test_returns_new_pair_and_revokes_old(self, auth_service, test_session):
        init_data = build_init_data(bot_token=TEST_BOT_TOKEN, telegram_id=TEST_TELEGRAM_ID)
        first = await auth_service.login(init_data=init_data)

        second = await auth_service.refresh(refresh_token=first.refresh_token)

        assert second.access_token
        assert second.refresh_token != first.refresh_token

        old_hash = jwt_service.hash_refresh(first.refresh_token)
        new_hash = jwt_service.hash_refresh(second.refresh_token)

        old_row = await RefreshTokenRepository(test_session).find_by_hash(old_hash)
        new_row = await RefreshTokenRepository(test_session).find_by_hash(new_hash)
        assert old_row.revoked_at is not None
        assert old_row.replaced_by == new_hash
        assert new_row is not None
        assert new_row.revoked_at is None

    async def test_rejects_invalid_token(self, auth_service):
        with pytest.raises(UnauthorizedError, match="invalid_refresh_token"):
            await auth_service.refresh(refresh_token="bogus-token-value")

    async def test_rejects_expired_token(self, auth_service, test_session, test_user):
        raw = jwt_service.generate_refresh_token()
        token_row = RefreshToken(
            user_id=test_user.id,
            token_hash=jwt_service.hash_refresh(raw),
            expires_at=datetime.now(UTC) - timedelta(seconds=1),
        )
        test_session.add(token_row)
        await test_session.commit()

        with pytest.raises(UnauthorizedError, match="refresh_token_expired"):
            await auth_service.refresh(refresh_token=raw)

    async def test_detects_reuse_and_revokes_all_user_tokens(
        self, auth_service, test_session
    ):
        init_data = build_init_data(bot_token=TEST_BOT_TOKEN, telegram_id=TEST_TELEGRAM_ID)
        first = await auth_service.login(init_data=init_data)
        await auth_service.login(init_data=init_data)

        await auth_service.refresh(refresh_token=first.refresh_token)

        with pytest.raises(UnauthorizedError, match="refresh_token_reused"):
            await auth_service.refresh(refresh_token=first.refresh_token)

        test_session.expire_all()
        rows = (await test_session.execute(select(RefreshToken))).scalars().all()
        assert all(r.revoked_at is not None for r in rows)

    async def test_rejects_blocked_user(self, auth_service, test_session):
        init_data = build_init_data(bot_token=TEST_BOT_TOKEN, telegram_id=TEST_TELEGRAM_ID)
        first = await auth_service.login(init_data=init_data)

        user = (
            await test_session.execute(
                select(User).where(User.telegram_id == TEST_TELEGRAM_ID)
            )
        ).scalar_one()
        user.is_blocked = True
        await test_session.commit()

        with pytest.raises(ForbiddenError, match="user_blocked"):
            await auth_service.refresh(refresh_token=first.refresh_token)


class TestLogout:
    async def test_revokes_submitted_token(self, auth_service, test_session):
        init_data = build_init_data(bot_token=TEST_BOT_TOKEN, telegram_id=TEST_TELEGRAM_ID)
        first = await auth_service.login(init_data=init_data)

        result = await auth_service.logout(refresh_token=first.refresh_token)
        assert result is True

        row = await RefreshTokenRepository(test_session).find_by_hash(
            jwt_service.hash_refresh(first.refresh_token)
        )
        assert row.revoked_at is not None

    async def test_is_idempotent_on_missing_token(self, auth_service):
        result = await auth_service.logout(refresh_token="non-existent-refresh-value")
        assert result is False
