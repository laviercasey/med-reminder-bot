from datetime import UTC, datetime, timedelta

from httpx import AsyncClient
from sqlalchemy import select

from api.core.config import api_config
from api.services.auth import jwt_service
from shared.database.models import RefreshToken, User
from tests.conftest import TEST_ADMIN_TELEGRAM_ID, TestSessionLocal


class TestAdminStats:
    async def test_returns_statistics(self, admin_client: AsyncClient):
        resp = await admin_client.get("/api/admin/stats")
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        data = body["data"]
        assert "total_users" in data
        assert "active_users" in data
        assert "avg_pills" in data
        assert isinstance(data["total_users"], int)


class TestNonAdminForbidden:
    async def test_stats_forbidden_for_regular_user(self, test_client: AsyncClient):
        resp = await test_client.get("/api/admin/stats")
        assert resp.status_code == 403

    async def test_users_forbidden_for_regular_user(self, test_client: AsyncClient):
        resp = await test_client.get("/api/admin/users")
        assert resp.status_code == 403

    async def test_ban_forbidden_for_regular_user(self, test_client: AsyncClient):
        resp = await test_client.post(
            "/api/admin/ban",
            json={"telegram_id": 111},
        )
        assert resp.status_code == 403


class TestAdminBanUser:
    async def test_ban_existing_user(self, admin_client: AsyncClient):
        resp = await admin_client.post(
            "/api/admin/ban",
            json={"telegram_id": TEST_ADMIN_TELEGRAM_ID},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_ban_nonexistent_user(self, admin_client: AsyncClient):
        resp = await admin_client.post(
            "/api/admin/ban",
            json={"telegram_id": 777777777},
        )
        assert resp.status_code == 404
        assert resp.json()["error"] == "user_not_found"


class TestBanRevokesRefreshTokens:
    async def test_ban_revokes_all_refresh_tokens_for_target_user(
        self, admin_client: AsyncClient
    ):
        async with TestSessionLocal() as session:
            target = User(telegram_id=555444333, language="en", is_blocked=False)
            session.add(target)
            await session.commit()

            raw_a = jwt_service.generate_refresh_token()
            raw_b = jwt_service.generate_refresh_token()
            for raw in (raw_a, raw_b):
                session.add(
                    RefreshToken(
                        user_id=target.id,
                        token_hash=jwt_service.hash_refresh(raw),
                        expires_at=datetime.now(UTC)
                        + timedelta(seconds=api_config.jwt_refresh_ttl),
                    )
                )
            await session.commit()
            target_id = target.id

        resp = await admin_client.post(
            "/api/admin/ban",
            json={"telegram_id": 555444333},
        )
        assert resp.status_code == 200

        async with TestSessionLocal() as session:
            rows = (
                await session.execute(
                    select(RefreshToken).where(RefreshToken.user_id == target_id)
                )
            ).scalars().all()
            assert len(rows) == 2
            assert all(r.revoked_at is not None for r in rows)


class TestAdminUnbanUser:
    async def test_unban_existing_user(self, admin_client: AsyncClient):
        await admin_client.post(
            "/api/admin/ban",
            json={"telegram_id": TEST_ADMIN_TELEGRAM_ID},
        )
        resp = await admin_client.post(
            "/api/admin/unban",
            json={"telegram_id": TEST_ADMIN_TELEGRAM_ID},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_unban_nonexistent_user(self, admin_client: AsyncClient):
        resp = await admin_client.post(
            "/api/admin/unban",
            json={"telegram_id": 777777777},
        )
        assert resp.status_code == 404
        assert resp.json()["error"] == "user_not_found"
