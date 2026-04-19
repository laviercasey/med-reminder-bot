import time
from typing import AsyncGenerator

import jwt as pyjwt
import pytest_asyncio
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from api import dependencies
from api.core.config import api_config
from api.core.exceptions import AppException
from api.core.response import ApiResponse
from api.services.auth import jwt_service
from shared.database.models import User
from tests.conftest import TestSessionLocal


def _make_probe_app():
    app = FastAPI()

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with TestSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[dependencies.get_session] = override_get_session

    @app.get("/whoami", response_model=ApiResponse[dict])
    async def whoami(user: User = Depends(dependencies.get_current_user)):
        return ApiResponse.ok({"id": user.id, "telegram_id": user.telegram_id})

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "data": None, "error": exc.message},
        )

    return app


@pytest_asyncio.fixture
async def probe_client(test_user) -> AsyncGenerator[AsyncClient, None]:
    app = _make_probe_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


class TestGetCurrentUser:
    async def test_accepts_valid_bearer_token(self, probe_client, test_user):
        token, _ = jwt_service.issue_access(test_user)
        resp = await probe_client.get(
            "/whoami",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["telegram_id"] == test_user.telegram_id

    async def test_rejects_missing_authorization(self, probe_client):
        resp = await probe_client.get("/whoami")
        assert resp.status_code == 401
        assert resp.json()["error"] == "missing_authorization"

    async def test_rejects_wrong_scheme(self, probe_client):
        resp = await probe_client.get(
            "/whoami",
            headers={"Authorization": "Basic foo"},
        )
        assert resp.status_code == 401
        assert resp.json()["error"] == "invalid_token_scheme"

    async def test_rejects_refresh_typed_token(self, probe_client, test_user):
        now = int(time.time())
        payload = {
            "sub": str(test_user.telegram_id),
            "uid": test_user.id,
            "type": "refresh",
            "iat": now,
            "exp": now + 900,
            "iss": api_config.jwt_issuer,
            "aud": api_config.jwt_audience,
        }
        token = pyjwt.encode(payload, api_config.jwt_secret, algorithm="HS256")
        resp = await probe_client.get(
            "/whoami",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 401
        assert resp.json()["error"] == "wrong_token_type"

    async def test_rejects_expired_token(self, probe_client, test_user, monkeypatch):
        real_time = time.time
        monkeypatch.setattr(
            jwt_service.time,
            "time",
            lambda: int(real_time()) - api_config.jwt_access_ttl - 60,
        )
        token, _ = jwt_service.issue_access(test_user)
        monkeypatch.setattr(jwt_service.time, "time", real_time)
        resp = await probe_client.get(
            "/whoami",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 401
        assert resp.json()["error"] == "token_expired"

    async def test_rejects_blocked_user(self, probe_client, test_user, test_session):
        test_user.is_blocked = True
        test_session.add(test_user)
        await test_session.commit()
        token, _ = jwt_service.issue_access(test_user)
        resp = await probe_client.get(
            "/whoami",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 403
        assert resp.json()["error"] == "user_blocked"

    async def test_rejects_invalid_token(self, probe_client):
        resp = await probe_client.get(
            "/whoami",
            headers={"Authorization": "Bearer not-a-valid-jwt"},
        )
        assert resp.status_code == 401
        assert resp.json()["error"] == "invalid_token"

    async def test_rejects_user_not_found(self, probe_client):
        ghost_user = User(id=99999, telegram_id=999000111)
        token, _ = jwt_service.issue_access(ghost_user)
        resp = await probe_client.get(
            "/whoami",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 401
        assert resp.json()["error"] == "user_not_found"
