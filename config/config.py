import os
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # Telegram Bot settings
    BOT_TOKEN: str
    ADMIN_IDS: List[int]
    PAYMENT_PROVIDER_TOKEN: str
    
    # Database settings
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    # Subscription prices (in kopecks)
    MONTHLY_PRICE: int = 9900
    YEARLY_PRICE: int = 79900
    LIFETIME_PRICE: int = 199900
    
    # Reminder settings
    REMINDER_RETRY_MINUTES: int = 30
    
    # Database URL
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Загружаем переменные окружения вручную
admin_ids_str = os.getenv("ADMIN_IDS", "")
admin_ids = []
if admin_ids_str:
    try:
        admin_ids = [int(id_str.strip()) for id_str in admin_ids_str.split(",") if id_str.strip()]
    except ValueError:
        admin_ids = []

settings = Settings(
    BOT_TOKEN=os.getenv("BOT_TOKEN", ""),
    ADMIN_IDS=admin_ids,
    PAYMENT_PROVIDER_TOKEN=os.getenv("PAYMENT_PROVIDER_TOKEN", ""),
    DB_HOST=os.getenv("DB_HOST", "localhost"),
    DB_PORT=int(os.getenv("DB_PORT", "5432")),
    DB_USER=os.getenv("DB_USER", ""),
    DB_PASS=os.getenv("DB_PASS", ""),
    DB_NAME=os.getenv("DB_NAME", "")
)
