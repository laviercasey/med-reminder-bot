from httpx import AsyncClient


class TestGetSettings:
    async def test_returns_default_settings(self, test_client: AsyncClient):
        resp = await test_client.get("/api/settings")
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert body["data"]["reminders_enabled"] is True
        assert body["data"]["reminder_repeat_minutes"] == 30
        assert body["data"]["language"] == "en"


class TestUpdateLanguage:
    async def test_update_to_russian(self, test_client: AsyncClient):
        resp = await test_client.patch(
            "/api/settings",
            json={"language": "ru"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert body["data"]["language"] == "ru"

    async def test_invalid_language_rejected(self, test_client: AsyncClient):
        resp = await test_client.patch(
            "/api/settings",
            json={"language": "fr"},
        )
        assert resp.status_code == 422

    async def test_update_back_to_english(self, test_client: AsyncClient):
        await test_client.patch("/api/settings", json={"language": "ru"})
        resp = await test_client.patch("/api/settings", json={"language": "en"})
        assert resp.status_code == 200
        assert resp.json()["data"]["language"] == "en"


class TestUpdateReminders:
    async def test_disable_reminders(self, test_client: AsyncClient):
        resp = await test_client.patch(
            "/api/settings",
            json={"reminders_enabled": False},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["reminders_enabled"] is False

    async def test_change_repeat_minutes(self, test_client: AsyncClient):
        resp = await test_client.patch(
            "/api/settings",
            json={"reminder_repeat_minutes": 15},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["reminder_repeat_minutes"] == 15

    async def test_repeat_minutes_min_validation(self, test_client: AsyncClient):
        resp = await test_client.patch(
            "/api/settings",
            json={"reminder_repeat_minutes": 0},
        )
        assert resp.status_code == 422

    async def test_repeat_minutes_max_validation(self, test_client: AsyncClient):
        resp = await test_client.patch(
            "/api/settings",
            json={"reminder_repeat_minutes": 120},
        )
        assert resp.status_code == 422

    async def test_update_multiple_fields(self, test_client: AsyncClient):
        resp = await test_client.patch(
            "/api/settings",
            json={
                "reminders_enabled": False,
                "reminder_repeat_minutes": 10,
                "language": "ru",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["reminders_enabled"] is False
        assert body["data"]["reminder_repeat_minutes"] == 10
        assert body["data"]["language"] == "ru"
