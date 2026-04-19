from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    BOT_TOKEN: str
    ADMIN_IDS: list[int] = []

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        if isinstance(v, int):
            return [v]
        return v

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_URL: str = "redis://localhost:6379/0"
    MINI_APP_URL: str = ""
    DOMAIN: str = ""

    REMINDER_RETRY_MINUTES: int = 30

    API_PORT: int = 8000
    ENVIRONMENT: str = "production"

    JWT_SECRET: str
    JWT_ACCESS_TTL_SECONDS: int = 900
    JWT_REFRESH_TTL_SECONDS: int = 604800
    JWT_ISSUER: str = "med-reminder-api"
    JWT_AUDIENCE: str = "med-reminder-miniapp"

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


settings = Settings()
