import os

from shared.config import Settings
from shared.config import settings as shared_settings


class ApiConfig:
    def __init__(self, base_settings: Settings):
        self._settings = base_settings
        self.cors_origins: list[str] = self._parse_cors_origins()
        self.api_prefix: str = "/api"
        self.rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        self.max_auth_age: int = int(os.getenv("MAX_AUTH_AGE", "86400"))

    def _parse_cors_origins(self) -> list[str]:
        origins_str = os.getenv("CORS_ORIGINS", "")
        if origins_str:
            return [o.strip() for o in origins_str.split(",") if o.strip()]
        if self._settings.MINI_APP_URL:
            return [self._settings.MINI_APP_URL]
        if os.getenv("ENVIRONMENT") == "development":
            return ["*"]
        raise RuntimeError("CORS_ORIGINS or MINI_APP_URL must be set")

    @property
    def bot_token(self) -> str:
        return self._settings.BOT_TOKEN

    @property
    def database_url(self):
        return self._settings.database_url

    @property
    def redis_url(self) -> str:
        return self._settings.REDIS_URL

    @property
    def admin_ids(self) -> list[int]:
        return self._settings.ADMIN_IDS

    @property
    def mini_app_url(self) -> str:
        return self._settings.MINI_APP_URL

    @property
    def domain(self) -> str:
        return self._settings.DOMAIN


api_config = ApiConfig(shared_settings)
