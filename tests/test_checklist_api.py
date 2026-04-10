from datetime import date

from httpx import AsyncClient


class TestGetTodayChecklist:
    async def test_empty_checklist(self, test_client: AsyncClient):
        resp = await test_client.get("/api/checklist")
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert body["data"]["items"] == []
        assert body["data"]["total"] == 0
        assert body["data"]["taken"] == 0

    async def test_checklist_with_medications(self, test_client: AsyncClient):
        await test_client.post(
            "/api/medications",
            json={"name": "Morning Pill", "schedule": "morning", "time": "08:00"},
        )

        resp = await test_client.get("/api/checklist")
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["total"] == 1
        assert body["data"]["taken"] == 0
        assert body["data"]["items"][0]["medication_name"] == "Morning Pill"
        assert body["data"]["items"][0]["status"] is False

    async def test_checklist_with_date_param(self, test_client: AsyncClient):
        await test_client.post(
            "/api/medications",
            json={"name": "Pill", "schedule": "morning", "time": "08:00"},
        )
        today = date.today().isoformat()
        resp = await test_client.get(f"/api/checklist?date={today}")
        assert resp.status_code == 200
        assert resp.json()["data"]["date"] == today


class TestMarkTaken:
    async def test_mark_taken(self, test_client: AsyncClient):
        await test_client.post(
            "/api/medications",
            json={"name": "Pill", "schedule": "morning", "time": "08:00"},
        )
        checklist_resp = await test_client.get("/api/checklist")
        item_id = checklist_resp.json()["data"]["items"][0]["id"]

        resp = await test_client.patch(
            f"/api/checklist/{item_id}",
            json={"status": True},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True

        verify_resp = await test_client.get("/api/checklist")
        assert verify_resp.json()["data"]["taken"] == 1
        assert verify_resp.json()["data"]["items"][0]["status"] is True


class TestMarkUntaken:
    async def test_mark_untaken(self, test_client: AsyncClient):
        await test_client.post(
            "/api/medications",
            json={"name": "Pill", "schedule": "morning", "time": "08:00"},
        )
        checklist_resp = await test_client.get("/api/checklist")
        item_id = checklist_resp.json()["data"]["items"][0]["id"]

        await test_client.patch(
            f"/api/checklist/{item_id}",
            json={"status": True},
        )

        resp = await test_client.patch(
            f"/api/checklist/{item_id}",
            json={"status": False},
        )
        assert resp.status_code == 200

        verify_resp = await test_client.get("/api/checklist")
        assert verify_resp.json()["data"]["taken"] == 0
        assert verify_resp.json()["data"]["items"][0]["status"] is False


class TestMarkTakenNotFound:
    async def test_returns_404(self, test_client: AsyncClient):
        resp = await test_client.patch(
            "/api/checklist/99999",
            json={"status": True},
        )
        assert resp.status_code == 404
        body = resp.json()
        assert body["success"] is False
        assert body["error"] == "checklist_item_not_found"
