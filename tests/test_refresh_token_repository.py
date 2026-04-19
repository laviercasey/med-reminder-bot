from datetime import UTC, datetime, timedelta

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.auth.repository import RefreshTokenRepository
from shared.database.models import User


@pytest_asyncio.fixture
async def repo(test_session: AsyncSession) -> RefreshTokenRepository:
    return RefreshTokenRepository(test_session)


@pytest_asyncio.fixture
async def other_user(test_session: AsyncSession) -> User:
    user = User(telegram_id=222222222, language="en", is_blocked=False)
    test_session.add(user)
    await test_session.commit()
    return user


class TestCreate:
    async def test_persists_row(self, repo, test_user, test_session):
        expires = datetime.now(UTC) + timedelta(days=7)
        token = await repo.create(
            user_id=test_user.id,
            token_hash="a" * 64,
            expires_at=expires,
            user_agent="test-agent",
        )
        assert token.id is not None
        assert token.token_hash == "a" * 64
        assert token.user_id == test_user.id
        assert token.user_agent == "test-agent"
        assert token.revoked_at is None
        assert token.replaced_by is None


class TestFindByHash:
    async def test_returns_active_token(self, repo, test_user):
        expires = datetime.now(UTC) + timedelta(days=7)
        await repo.create(
            user_id=test_user.id, token_hash="b" * 64, expires_at=expires
        )
        found = await repo.find_by_hash("b" * 64)
        assert found is not None
        assert found.token_hash == "b" * 64

    async def test_returns_none_for_missing(self, repo):
        found = await repo.find_by_hash("c" * 64)
        assert found is None


class TestRevoke:
    async def test_sets_revoked_at_and_replaced_by(self, repo, test_user, test_session):
        expires = datetime.now(UTC) + timedelta(days=7)
        token = await repo.create(
            user_id=test_user.id, token_hash="d" * 64, expires_at=expires
        )
        await repo.revoke(token, replaced_by="e" * 64)
        await test_session.refresh(token)
        assert token.revoked_at is not None
        assert token.replaced_by == "e" * 64


class TestRevokeAllForUser:
    async def test_sets_revoked_at_on_active_only(
        self, repo, test_user, other_user, test_session
    ):
        expires = datetime.now(UTC) + timedelta(days=7)
        active1 = await repo.create(
            user_id=test_user.id, token_hash="1" * 64, expires_at=expires
        )
        active2 = await repo.create(
            user_id=test_user.id, token_hash="2" * 64, expires_at=expires
        )
        already_revoked = await repo.create(
            user_id=test_user.id, token_hash="3" * 64, expires_at=expires
        )
        original_revoke_time = datetime.now(UTC) - timedelta(days=1)
        already_revoked.revoked_at = original_revoke_time
        await test_session.flush()

        other_token = await repo.create(
            user_id=other_user.id, token_hash="4" * 64, expires_at=expires
        )

        await repo.revoke_all_for_user(test_user.id)

        await test_session.refresh(active1)
        await test_session.refresh(active2)
        await test_session.refresh(already_revoked)
        await test_session.refresh(other_token)

        assert active1.revoked_at is not None
        assert active2.revoked_at is not None
        assert already_revoked.revoked_at is not None
        assert abs(
            (already_revoked.revoked_at.replace(tzinfo=UTC) - original_revoke_time).total_seconds()
        ) < 5
        assert other_token.revoked_at is None
