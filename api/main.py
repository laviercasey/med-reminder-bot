import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from starlette.middleware.base import BaseHTTPMiddleware

from api.core.config import api_config
from api.core.exceptions import AppException
from api.middleware.rate_limit import RateLimitMiddleware
from api.services.admin.router import router as admin_router
from api.services.auth.router import router as auth_router
from api.services.checklist.router import router as checklist_router
from api.services.medication.router import router as medication_router
from api.services.settings.router import router as settings_router
from api.services.user.router import router as user_router
from shared.database import db as _db
from shared.database.db import configure_engine
from shared.logging import setup_logger
from shared.redis import close_redis_client, get_redis_client

logger = setup_logger("med_reminder_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_engine(api_config.database_url)
    logger.info("API started")
    yield
    await close_redis_client()
    logger.info("API stopped")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "%s %s %s %.2fms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            extra={
                "extra": {
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                }
            },
        )
        return response


def create_app() -> FastAPI:
    app = FastAPI(
        title="MedReminder API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware, requests_per_minute=api_config.rate_limit_per_minute)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_config.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.include_router(auth_router, prefix="/api")
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
        result = {"status": "ok", "database": "ok", "redis": "ok"}

        try:
            async with _db.async_session_maker() as session:
                await session.execute(text("SELECT 1"))
        except Exception as exc:
            logger.warning("Health check database probe failed: %s", exc)
            result["database"] = "unavailable"
            result["status"] = "degraded"

        try:
            redis = await get_redis_client()
            await redis.ping()
        except Exception as exc:
            logger.warning("Health check Redis probe failed: %s", exc)
            result["redis"] = "unavailable"
            result["status"] = "degraded"

        return result

    return app


app = create_app()
