from httpx import AsyncClient

from tests.conftest import TEST_TELEGRAM_ID


class TestGetMe:
    async def test_returns_user_profile(self, test_client: AsyncClient):
        resp = await test_client.get("/api/me")
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        data = body["data"]
        assert data["telegram_id"] == TEST_TELEGRAM_ID
        assert data["language"] == "en"
        assert data["medications_count"] == 0

    async def test_medications_count_reflects_actual(self, test_client: AsyncClient):
        await test_client.post(
            "/api/medications",
            json={"name": "Med1", "schedule": "morning", "time": "08:00"},
        )
        await test_client.post(
            "/api/medications",
            json={"name": "Med2", "schedule": "evening", "time": "20:00"},
        )

        resp = await test_client.get("/api/me")
        body = resp.json()
        assert body["data"]["medications_count"] == 2

    async def test_premium_user_profile(self, premium_client: AsyncClient):
        resp = await premium_client.get("/api/me")
        body = resp.json()
        assert body["success"] is True
