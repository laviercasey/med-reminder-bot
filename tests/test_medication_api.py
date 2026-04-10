from httpx import AsyncClient


class TestListMedicationsEmpty:
    async def test_returns_empty_list(self, test_client: AsyncClient):
        resp = await test_client.get("/api/medications")
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert body["data"]["medications"] == []
        assert body["data"]["count"] == 0


class TestCreateMedication:
    async def test_success(self, test_client: AsyncClient):
        payload = {"name": "Aspirin", "schedule": "morning", "time": "08:00"}
        resp = await test_client.post("/api/medications", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["success"] is True
        assert body["data"]["name"] == "Aspirin"
        assert body["data"]["schedule"] == "morning"
        assert body["data"]["time"] == "08:00"
        assert "id" in body["data"]

    async def test_validates_time_format(self, test_client: AsyncClient):
        payload = {"name": "Aspirin", "schedule": "morning", "time": "invalid"}
        resp = await test_client.post("/api/medications", json=payload)
        assert resp.status_code == 422

    async def test_validates_schedule_value(self, test_client: AsyncClient):
        payload = {"name": "Aspirin", "schedule": "midnight", "time": "08:00"}
        resp = await test_client.post("/api/medications", json=payload)
        assert resp.status_code == 422

    async def test_validates_name_required(self, test_client: AsyncClient):
        payload = {"schedule": "morning", "time": "08:00"}
        resp = await test_client.post("/api/medications", json=payload)
        assert resp.status_code == 422

    async def test_validates_name_not_empty(self, test_client: AsyncClient):
        payload = {"name": "", "schedule": "morning", "time": "08:00"}
        resp = await test_client.post("/api/medications", json=payload)
        assert resp.status_code == 422


class TestDeleteMedication:
    async def test_success(self, test_client: AsyncClient):
        create_resp = await test_client.post(
            "/api/medications",
            json={"name": "ToDelete", "schedule": "evening", "time": "20:00"},
        )
        med_id = create_resp.json()["data"]["id"]

        resp = await test_client.delete(f"/api/medications/{med_id}")
        assert resp.status_code == 200
        assert resp.json()["success"] is True

        list_resp = await test_client.get("/api/medications")
        assert list_resp.json()["data"]["count"] == 0

    async def test_not_found(self, test_client: AsyncClient):
        resp = await test_client.delete("/api/medications/99999")
        assert resp.status_code == 404
        body = resp.json()
        assert body["success"] is False
        assert body["error"] == "medication_not_found"
