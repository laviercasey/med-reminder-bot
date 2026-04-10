from httpx import AsyncClient

from tests.conftest import TEST_ADMIN_TELEGRAM_ID


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
