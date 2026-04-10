import ipaddress
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from shared.logging import setup_logger
from shared.redis import get_redis_client

logger = setup_logger("rate_limit")

TRUSTED_PROXIES = {
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
}


def _is_trusted_proxy(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(addr in net for net in TRUSTED_PROXIES)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self._requests_per_minute = requests_per_minute
        self._window = 60.0

    def _get_client_key(self, request: Request) -> str:
        client_ip = request.client.host if request.client else "unknown"
        if _is_trusted_proxy(client_ip):
            forwarded = request.headers.get("x-forwarded-for")
            if forwarded:
                return forwarded.split(",")[0].strip()
        return client_ip

    async def _is_rate_limited(self, key: str) -> bool:
        try:
            redis = await get_redis_client()
            now = time.time()
            window_start = now - self._window
            redis_key = f"rl:{key}"
            pipe = redis.pipeline()
            pipe.zremrangebyscore(redis_key, 0, window_start)
            pipe.zadd(redis_key, {str(now): now})
            pipe.zcard(redis_key)
            pipe.expire(redis_key, int(self._window) + 1)
            _, _, count, _ = await pipe.execute()
            return count > self._requests_per_minute
        except Exception as exc:
            logger.warning("Rate limiter Redis error, allowing request: %s", exc)
            return False

    async def dispatch(self, request: Request, call_next):
        client_key = self._get_client_key(request)

        if await self._is_rate_limited(client_key):
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "data": None,
                    "error": "rate_limit_exceeded",
                },
            )

        response = await call_next(request)
        return response
