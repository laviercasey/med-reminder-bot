import hashlib
import hmac
import json
import time
import urllib.parse
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from shared.database.db import Base
from shared.database.models import User

TEST_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz_0123456789"
TEST_TELEGRAM_ID = 123456789
TEST_ADMIN_TELEGRAM_ID = 999999999


def build_init_data(
    bot_token: str,
    telegram_id: int,
    first_name: str = "Test",
    last_name: str = "User",
    username: str = "testuser",
    language_code: str = "en",
    auth_date: int | None = None,
) -> str:
    if auth_date is None:
        auth_date = int(time.time())

    user_data = json.dumps(
        {
            "id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "language_code": language_code,
        },
        separators=(",", ":"),
    )

    params = {
        "user": user_data,
        "auth_date": str(auth_date),
    }

    data_check_pairs = []
    for key in sorted(params.keys()):
        data_check_pairs.append(f"{key}={params[key]}")
    data_check_string = "\n".join(data_check_pairs)

    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    params["hash"] = computed_hash
    return urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


engine = create_async_engine(
    "sqlite+aiosqlite://",
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@pytest_asyncio.fixture
async def test_user(test_session: AsyncSession) -> User:
    user = User(
        telegram_id=TEST_TELEGRAM_ID,
        language="en",
        is_blocked=False,
    )
    test_session.add(user)
    await test_session.commit()
    return user


@pytest_asyncio.fixture
async def test_admin(test_session: AsyncSession) -> User:
    admin = User(
        telegram_id=TEST_ADMIN_TELEGRAM_ID,
        language="en",
        is_blocked=False,
    )
    test_session.add(admin)
    await test_session.commit()
    return admin


@pytest_asyncio.fixture
async def premium_user(test_session: AsyncSession) -> User:
    user = User(
        telegram_id=TEST_TELEGRAM_ID,
        language="en",
        is_blocked=False,
    )
    test_session.add(user)
    await test_session.commit()
    return user


@pytest.fixture
def valid_init_data():
    def _build(
        telegram_id: int = TEST_TELEGRAM_ID,
        auth_date: int | None = None,
    ) -> str:
        return build_init_data(
            bot_token=TEST_BOT_TOKEN,
            telegram_id=telegram_id,
            auth_date=auth_date,
        )

    return _build


@pytest.fixture
def auth_headers(valid_init_data) -> dict[str, str]:
    return {"Authorization": f"tma {valid_init_data()}"}


@pytest.fixture
def admin_auth_headers(valid_init_data) -> dict[str, str]:
    return {"Authorization": f"tma {valid_init_data(telegram_id=TEST_ADMIN_TELEGRAM_ID)}"}


def _create_test_app(
    override_user: User | None = None,
    override_admin: User | None = None,
    session_factory: async_sessionmaker | None = None,
):
    import os

    os.environ.setdefault("BOT_TOKEN", TEST_BOT_TOKEN)
    os.environ.setdefault("ADMIN_IDS", str(TEST_ADMIN_TELEGRAM_ID))

    from api.core.config import api_config

    api_config._settings.ADMIN_IDS = [TEST_ADMIN_TELEGRAM_ID]

    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse

    from api import dependencies
    from api.core.exceptions import AppException
    from api.services.admin.router import router as admin_router
    from api.services.checklist.router import router as checklist_router
    from api.services.medication.router import router as medication_router
    from api.services.settings.router import router as settings_router
    from api.services.user.router import router as user_router

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

    from unittest.mock import AsyncMock

    from api.services.pubsub.publisher import RedisPublisher

    mock_redis = AsyncMock()
    mock_publisher = RedisPublisher(mock_redis)
    app.dependency_overrides[dependencies.get_publisher] = lambda: mock_publisher

    if override_user is not None:
        app.dependency_overrides[dependencies.get_current_user] = lambda: override_user

    if override_admin is not None:
        app.dependency_overrides[dependencies.require_admin] = lambda: override_admin

    app.include_router(medication_router, prefix="/api")
    app.include_router(checklist_router, prefix="/api")
    app.include_router(settings_router, prefix="/api")
    app.include_router(user_router, prefix="/api")
    app.include_router(admin_router, prefix="/api")

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "data": None,
                "error": exc.message,
            },
        )

    @app.get("/api/health")
    async def health_check():
        return {"status": "ok"}

    return app


@pytest_asyncio.fixture
async def test_app(test_user: User):
    app = _create_test_app(override_user=test_user)
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_app(test_admin: User):
    app = _create_test_app(override_user=test_admin, override_admin=test_admin)
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def premium_app(premium_user: User):
    app = _create_test_app(override_user=premium_user)
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_client(test_app) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def admin_client(admin_app) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=admin_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def premium_client(premium_app) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=premium_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
