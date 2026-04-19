from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tests.conftest import (
    TEST_BOT_TOKEN,
    TEST_TELEGRAM_ID,
    TestSessionLocal,
    build_init_data,
)


def _build_auth_app(session_factory: async_sessionmaker | None = None):
    import os

    os.environ.setdefault("BOT_TOKEN", TEST_BOT_TOKEN)

    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse

    from api import dependencies
    from api.core.exceptions import AppException
    from api.services.auth.router import router as auth_router

    app = FastAPI()

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        factory = session_factory or TestSessionLocal
        async with factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[dependencies.get_session] = override_get_session

    app.include_router(auth_router, prefix="/api")

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "data": None, "error": exc.message},
        )

    return app


@pytest_asyncio.fixture
async def auth_app():
    app = _build_auth_app()
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_client(auth_app) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=auth_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


class TestLoginEndpoint:
    async def test_returns_token_pair(self, auth_client: AsyncClient, valid_init_data):
        resp = await auth_client.post(
            "/api/auth/login",
            json={"init_data": valid_init_data()},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        data = body["data"]
        assert data["access_token"]
        assert data["refresh_token"]
        assert data["token_type"] == "Bearer"
        assert isinstance(data["expires_in"], int)
        assert isinstance(data["expires_at"], int)
        assert isinstance(data["refresh_expires_at"], int)

    async def test_rejects_tampered_init_data(self, auth_client: AsyncClient, valid_init_data):
        init_data = valid_init_data()
        tampered = init_data.replace(init_data.split("hash=")[1][:10], "0000000000")
        resp = await auth_client.post(
            "/api/auth/login",
            json={"init_data": tampered},
        )
        assert resp.status_code == 401
        assert resp.json()["error"] == "invalid_hash"


class TestRefreshEndpoint:
    async def test_rotates_tokens(self, auth_client: AsyncClient, valid_init_data):
        login = await auth_client.post(
            "/api/auth/login",
            json={"init_data": valid_init_data()},
        )
        first = login.json()["data"]

        resp = await auth_client.post(
            "/api/auth/refresh",
            json={"refresh_token": first["refresh_token"]},
        )
        assert resp.status_code == 200
        second = resp.json()["data"]
        assert second["refresh_token"] != first["refresh_token"]
        assert second["access_token"]

    async def test_sets_success_false_on_reused_token(
        self, auth_client: AsyncClient, valid_init_data
    ):
        login = await auth_client.post(
            "/api/auth/login",
            json={"init_data": valid_init_data()},
        )
        first = login.json()["data"]

        await auth_client.post(
            "/api/auth/refresh",
            json={"refresh_token": first["refresh_token"]},
        )
        reuse = await auth_client.post(
            "/api/auth/refresh",
            json={"refresh_token": first["refresh_token"]},
        )
        assert reuse.status_code == 401
        body = reuse.json()
        assert body["success"] is False
        assert body["error"] == "refresh_token_reused"


class TestLogoutEndpoint:
    async def test_requires_bearer_token(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            "/api/auth/logout",
            json={"refresh_token": "irrelevant-value-aaaaaaaaaaaaa"},
        )
        assert resp.status_code == 401
        assert resp.json()["error"] in {"missing_authorization", "invalid_token"}

    async def test_returns_ok_for_unknown_refresh_token(
        self, auth_client: AsyncClient, valid_init_data
    ):
        login = await auth_client.post(
            "/api/auth/login",
            json={"init_data": valid_init_data()},
        )
        access = login.json()["data"]["access_token"]

        resp = await auth_client.post(
            "/api/auth/logout",
            json={"refresh_token": "unknown-refresh-token-value-12345"},
            headers={"Authorization": f"Bearer {access}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert body["data"]["revoked"] is False
