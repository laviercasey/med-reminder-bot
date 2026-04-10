from httpx import AsyncClient


class TestHealthEndpoint:
    async def test_returns_ok(self, test_client: AsyncClient):
        resp = await test_client.get("/api/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
