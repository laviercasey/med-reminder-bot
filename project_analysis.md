# PROJECT ANALYSIS DOCUMENT

*This document was automatically generated for AI analysis*

**Project Directory:** `/home/ksylika/Документы/med_reminder_bot`  
**Analysis Date:** 2025-07-21T00:04:32.704552  
**Total Files Analyzed:** 27  

## PROJECT STRUCTURE

```
{
  "handlers": {
    "pills.py": "pills.py",
    "admin.py": "admin.py",
    "reminders.py": "reminders.py",
    "settings.py": "settings.py",
    "start.py": "start.py",
    "ads.py": "ads.py",
    "checklist.py": "checklist.py",
    "__init__.py": "__init__.py"
  },
  ".env": ".env",
  "project_analyzer.py": "project_analyzer.py",
  "services": {
    "admin.py": "admin.py",
    "payments.py": "payments.py",
    "reminders.py": "reminders.py",
    "__init__.py": "__init__.py"
  },
  "utils": {
    "localization.py": "localization.py",
    "logger.py": "logger.py",
    "states.py": "states.py",
    "keyboards.py": "keyboards.py",
    "__init__.py": "__init__.py"
  },
  "config": {
    "config.py": "config.py",
    "__init__.py": "__init__.py"
  },
  "database": {
    "db.py": "db.py",
    "models.py": "models.py",
    "__init__.py": "__init__.py"
  },
  "bot.py": "bot.py",
  "migrations": {
    "versions": {
      "5a6c0bb5c0b5_create_tables.py": "5a6c0bb5c0b5_create_tables.py"
    },
    "env.py": "env.py",
    "README": "README",
    "script.py.mako": "script.py.mako"
  },
  "logs": {
    "bot_2025-04-02.log": "bot_2025-04-02.log",
    "bot_2025-04-03.log": "bot_2025-04-03.log"
  },
  "requirements.txt": "requirements.txt",
  "alembic.ini": "alembic.ini"
}
```

## FILE SUMMARY

| File Path | Language | Size | Description |
| --- | --- | --- | --- |
| `alembic.ini` | INI | 3.2 KB | # A generic, single database configuration. |
| `bot.py` | Python | 1.8 KB | Configure logging |
| `config/__init__.py` | Python | N/A | Empty file |
| `config/config.py` | Python | 1.4 KB | Telegram Bot settings |
| `database/__init__.py` | Python | N/A | Empty file |
| `database/db.py` | Python | 1.0 KB | Initialize the database |
| `database/models.py` | Python | 4.1 KB | Check if user has an active subscription |
| `handlers/__init__.py` | Python | 0.5 KB | Setup all handlers |
| `handlers/admin.py` | Python | 10.1 KB | Handle admin command - only accessible to admins |
| `handlers/ads.py` | Python | 4.9 KB | Handle subscription command |
| `handlers/checklist.py` | Python | 9.1 KB | Handle showing today's medication checklist |
| `handlers/pills.py` | Python | 19.5 KB | Handle add pill command |
| `handlers/reminders.py` | Python | 4.8 KB | Process snooze request |
| `handlers/settings.py` | Python | 9.1 KB | Handle settings command |
| `handlers/start.py` | Python | 3.6 KB | Handle /start command |
| `migrations/env.py` | Python | 2.4 KB | Run migrations in 'offline' mode. |
| `migrations/versions/5a6c0bb5c0b5_create_tables.py` | Python | 3.4 KB | create tables |
| `project_analyzer.py` | Python | 19.3 KB | Enhanced Project Structure Analyzer for AI Read... |
| `services/__init__.py` | Python | N/A | Empty file |
| `services/admin.py` | Python | 6.2 KB | Get statistics for admin panel |
| `services/payments.py` | Python | 4.3 KB | Check if user has an active premium subscription |
| `services/reminders.py` | Python | 13.8 KB | Setup daily reminder jobs |
| `utils/__init__.py` | Python | N/A | Empty file |
| `utils/keyboards.py` | Python | 6.7 KB | Get keyboard for settings menu |
| `utils/localization.py` | Python | 12.1 KB | from typing import Dict, Any |
| `utils/logger.py` | Python | 1.2 KB | Configure logging |
| `utils/states.py` | Python | 0.4 KB | from aiogram.fsm.state import State, StatesGroup |

## DEPENDENCIES AND IMPORTS

```json
{
  "project_analyzer.py": [
    "os",
    "argparse",
    "re",
    "json",
    "Path",
    "List",
    "datetime",
    "hashlib",
    "statements",
    "blocks",
    "pathlib",
    "typing"
  ],
  "bot.py": [
    "asyncio",
    "logging",
    "Bot",
    "ParseMode",
    "MemoryStorage",
    "settings",
    "setup_routers",
    "init_db",
    "setup_daily_reminders",
    "log_info",
    "get_session",
    "User",
    "select",
    "aiogram",
    "aiogram.enums",
    "aiogram.fsm.storage.memory",
    "config.config",
    "handlers",
    "database.db",
    "services.reminders",
    "utils.logger",
    "database.db",
    "database.models",
    "sqlalchemy"
  ],
  "handlers/pills.py": [
    "Router",
    "Command",
    "FSMContext",
    "select",
    "User",
    "get_session",
    "get_text",
    "get_schedule_keyboard",
    "AddPillStates",
    "log_user_action",
    "datetime",
    "re",
    "setup_medication_reminders",
    "Bot",
    "Checklist",
    "date",
    "Checklist",
    "date",
    "delete",
    "Checklist",
    "aiogram",
    "aiogram.filters",
    "aiogram.fsm.context",
    "sqlalchemy",
    "database.models",
    "database.db",
    "utils.localization",
    "utils.keyboards",
    "utils.states",
    "utils.logger",
    "datetime",
    "services.reminders",
    "aiogram",
    "database.models",
    "datetime",
    "database.models",
    "datetime",
    "sqlalchemy",
    "database.models"
  ],
  "handlers/admin.py": [
    "Router",
    "Command",
    "FSMContext",
    "select",
    "User",
    "get_session",
    "get_admin_keyboard",
    "AdminStates",
    "log_admin_action",
    "settings",
    "csv",
    "io",
    "aiogram",
    "aiogram.filters",
    "aiogram.fsm.context",
    "sqlalchemy",
    "database.models",
    "database.db",
    "utils.keyboards",
    "utils.states",
    "utils.logger",
    "config.config",
    "services.admin"
  ],
  "handlers/reminders.py": [
    "Router",
    "Command",
    "select",
    "User",
    "get_session",
    "get_text",
    "get_snooze_options_keyboard",
    "log_user_action",
    "datetime",
    "setup_daily_reminders",
    "is_premium_active",
    "DateTrigger",
    "scheduler",
    "aiogram",
    "aiogram.filters",
    "sqlalchemy",
    "database.models",
    "database.db",
    "utils.localization",
    "utils.keyboards",
    "utils.logger",
    "datetime",
    "services.reminders",
    "services.payments",
    "apscheduler.triggers.date",
    "services.reminders"
  ],
  "handlers/settings.py": [
    "Router",
    "Command",
    "FSMContext",
    "select",
    "User",
    "get_session",
    "get_text",
    "get_language_keyboard",
    "SettingsStates",
    "log_user_action",
    "UserSettings",
    "UserSettings",
    "UserSettings",
    "aiogram",
    "aiogram.filters",
    "aiogram.fsm.context",
    "sqlalchemy",
    "database.models",
    "database.db",
    "utils.localization",
    "utils.keyboards",
    "utils.states",
    "utils.logger",
    "database.models",
    "database.models",
    "database.models"
  ],
  "handlers/start.py": [
    "Router",
    "Command",
    "FSMContext",
    "select",
    "User",
    "get_session",
    "get_text",
    "get_language_keyboard",
    "log_user_action",
    "datetime",
    "aiogram",
    "aiogram.filters",
    "aiogram.fsm.context",
    "sqlalchemy",
    "database.models",
    "database.db",
    "utils.localization",
    "utils.keyboards",
    "utils.logger",
    "datetime"
  ],
  "handlers/ads.py": [
    "Router",
    "Command",
    "select",
    "User",
    "get_session",
    "get_text",
    "get_subscription_keyboard",
    "log_user_action",
    "is_premium_active",
    "settings",
    "datetime",
    "process_pre_checkout",
    "process_successful_payment",
    "aiogram",
    "aiogram.filters",
    "sqlalchemy",
    "database.models",
    "database.db",
    "utils.localization",
    "utils.keyboards",
    "utils.logger",
    "services.payments",
    "config.config",
    "datetime",
    "services.payments",
    "services.payments"
  ],
  "handlers/checklist.py": [
    "Router",
    "Command",
    "select",
    "User",
    "get_session",
    "get_text",
    "get_checklist_keyboard",
    "log_user_action",
    "datetime",
    "is_premium_active",
    "aiogram",
    "aiogram.filters",
    "sqlalchemy",
    "database.models",
    "database.db",
    "utils.localization",
    "utils.keyboards",
    "utils.logger",
    "datetime",
    "services.payments"
  ],
  "handlers/__init__.py": [
    "Router",
    "start",
    "aiogram",
    "."
  ],
  "services/admin.py": [
    "datetime",
    "select",
    "User",
    "get_session",
    "log_admin_action",
    "datetime",
    "sqlalchemy",
    "database.models",
    "database.db",
    "utils.logger"
  ],
  "services/payments.py": [
    "datetime",
    "select",
    "User",
    "get_session",
    "settings",
    "log_payment",
    "LabeledPrice",
    "datetime",
    "sqlalchemy",
    "database.models",
    "database.db",
    "config.config",
    "utils.logger",
    "aiogram.types"
  ],
  "services/reminders.py": [
    "datetime",
    "select",
    "AsyncIOScheduler",
    "CronTrigger",
    "User",
    "get_session",
    "Bot",
    "get_text",
    "get_checklist_keyboard",
    "log_info",
    "settings",
    "is_premium_active",
    "asyncio",
    "UserSettings",
    "UserSettings",
    "UserSettings",
    "datetime",
    "sqlalchemy",
    "apscheduler.schedulers.asyncio",
    "apscheduler.triggers.cron",
    "database.models",
    "database.db",
    "aiogram",
    "utils.localization",
    "utils.keyboards",
    "utils.logger",
    "config.config",
    "services.payments",
    "database.models",
    "database.models",
    "database.models"
  ],
  "utils/localization.py": [
    "Dict",
    "typing"
  ],
  "utils/logger.py": [
    "logging",
    "sys",
    "datetime",
    "datetime"
  ],
  "utils/states.py": [
    "State",
    "aiogram.fsm.state"
  ],
  "utils/keyboards.py": [
    "InlineKeyboardMarkup",
    "InlineKeyboardBuilder",
    "get_text",
    "datetime",
    "aiogram.types",
    "aiogram.utils.keyboard",
    "utils.localization",
    "datetime"
  ],
  "config/config.py": [
    "os",
    "List",
    "BaseModel",
    "load_dotenv",
    "typing",
    "pydantic",
    "dotenv"
  ],
  "database/db.py": [
    "create_async_engine",
    "DeclarativeBase",
    "settings",
    "AsyncGenerator",
    "asynccontextmanager",
    "sqlalchemy.ext.asyncio",
    "sqlalchemy.orm",
    "config.config",
    "typing",
    "contextlib"
  ],
  "database/models.py": [
    "Column",
    "relationship",
    "Base",
    "datetime",
    "sqlalchemy",
    "sqlalchemy.orm",
    "database.db",
    "datetime"
  ],
  "migrations/env.py": [
    "asyncio",
    "fileConfig",
    "pool",
    "Connection",
    "async_engine_from_config",
    "context",
    "create_async_engine",
    "settings",
    "Base",
    "create_engine",
    "logging.config",
    "sqlalchemy",
    "sqlalchemy.engine",
    "sqlalchemy.ext.asyncio",
    "alembic",
    "sqlalchemy.ext.asyncio",
    "config.config",
    "database.models",
    "sqlalchemy"
  ],
  "migrations/versions/5a6c0bb5c0b5_create_tables.py": [
    "Sequence",
    "op",
    "sqlalchemy",
    "typing",
    "alembic"
  ]
}
```

## FILE CONTENTS

> Note for AI: Each file is enclosed in a special marker format for easy parsing.
> BEGIN_FILE:{file_path} and END_FILE:{file_path}

### BEGIN_FILE:alembic.ini

**Path:** `alembic.ini`  
**Language:** INI  
**Description:** # A generic, single database configuration.  
**Last Modified:** 2025-04-02T14:01:46.289121  
**MD5 Hash:** 2b4d7d66c3dab37d1e97120926035edc  

```ini
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = migrations

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to migrations/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.
# version_locations = %(here)s/bar:%(here)s/bat:migrations/versions

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = postgresql://postgres:123@localhost:5432/med

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

```

### END_FILE:alembic.ini

### BEGIN_FILE:bot.py

**Path:** `bot.py`  
**Language:** Python  
**Description:** Configure logging  
**Last Modified:** 2025-04-02T15:44:08.764824  
**MD5 Hash:** dfd85303704ea736bcbef025b357ef74  

```python
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import settings
from handlers import setup_routers
from database.db import init_db
from services.reminders import setup_daily_reminders
from utils.logger import log_info
from database.db import get_session

async def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize bot and dispatcher
    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Setup handlers
    dp.include_router(setup_routers())
    
    # Initialize database
    log_info("Initializing database...")
    await init_db()
    
    # Initialize user settings for existing users
    async with get_session() as session:
        from database.models import User, UserSettings
        from sqlalchemy import select
        
        # Get all users without settings
        query = select(User).where(
            ~User.id.in_(select(UserSettings.user_id))
        )
        
        users_without_settings = (await session.execute(query)).scalars().all()
        
        # Create default settings for these users
        for user in users_without_settings:
            user_settings = UserSettings(
                user_id=user.id,
                reminders_enabled=True,
                reminder_repeat_minutes=30
            )
            session.add(user_settings)
        
        await session.commit()
    
    # Setup reminders
    await setup_daily_reminders(bot)

    # Start polling
    log_info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

```

### END_FILE:bot.py

### BEGIN_FILE:config/__init__.py

**Path:** `config/__init__.py`  
**Language:** Python  
**Description:** Empty file  
**Last Modified:** 2025-04-02T13:40:25.066085  
**MD5 Hash:** d41d8cd98f00b204e9800998ecf8427e  

```python

```

### END_FILE:config/__init__.py

### BEGIN_FILE:config/config.py

**Path:** `config/config.py`  
**Language:** Python  
**Description:** Telegram Bot settings  
**Last Modified:** 2025-04-02T14:01:01.534127  
**MD5 Hash:** 723159a2e7dec8ac7d05d6d91e19eb95  

```python
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

```

### END_FILE:config/config.py

### BEGIN_FILE:database/__init__.py

**Path:** `database/__init__.py`  
**Language:** Python  
**Description:** Empty file  
**Last Modified:** 2025-04-02T13:40:25.060086  
**MD5 Hash:** d41d8cd98f00b204e9800998ecf8427e  

```python

```

### END_FILE:database/__init__.py

### BEGIN_FILE:database/db.py

**Path:** `database/db.py`  
**Language:** Python  
**Description:** Initialize the database  
**Last Modified:** 2025-04-02T14:08:19.697311  
**MD5 Hash:** b734861932aa6cd370e5cf1272efc096  

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config.config import settings
from typing import AsyncGenerator
from contextlib import asynccontextmanager

# Create async engine
engine = create_async_engine(settings.database_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def init_db():
    """Initialize the database"""
    async with engine.begin() as conn:
        # Create tables if they don't exist
        # In production, use Alembic migrations instead
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

```

### END_FILE:database/db.py

### BEGIN_FILE:database/models.py

**Path:** `database/models.py`  
**Language:** Python  
**Description:** Check if user has an active subscription  
**Last Modified:** 2025-04-02T15:35:13.087318  
**MD5 Hash:** 0f36a658562737ffcc7ef68c655327b2  

```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Time, Date, func, Text, BigInteger as BigInt
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime, date, time

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInt, unique=True, nullable=False)  # Изменено с Integer на BigInt
    language = Column(String(2), default="en")
    is_premium = Column(Boolean, default=False)
    premium_until = Column(DateTime, nullable=True)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    medications = relationship("Medication", back_populates="user", cascade="all, delete-orphan")
    checklists = relationship("Checklist", back_populates="user", cascade="all, delete-orphan")
    
    def is_subscription_active(self) -> bool:
        """Check if user has an active subscription"""
        if not self.is_premium:
            return False
        
        # Lifetime subscription
        if self.premium_until is None:
            return True
        
        # Subscription with expiration date
        return datetime.utcnow() < self.premium_until

class Medication(Base):
    __tablename__ = "medications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    schedule = Column(String(20), nullable=False)  # "morning", "day", "evening", "custom"
    time = Column(Time, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="medications")
    checklists = relationship("Checklist", back_populates="medication", cascade="all, delete-orphan")

class Checklist(Base):
    __tablename__ = "checklist"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False)
    status = Column(Boolean, default=False)  # False = not taken, True = taken
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="checklists")
    medication = relationship("Medication", back_populates="checklists")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)  # Amount in kopecks
    subscription_type = Column(String(20), nullable=False)  # "monthly", "yearly", "lifetime"
    telegram_payment_id = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False)  # "pending", "completed", "failed"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")

class AdminLog(Base):
    __tablename__ = "admin_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSettings(Base):
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reminders_enabled = Column(Boolean, default=True)
    reminder_repeat_minutes = Column(Integer, default=30)  # 5, 15 или 30 минут
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", backref="settings")

```

### END_FILE:database/models.py

### BEGIN_FILE:handlers/__init__.py

**Path:** `handlers/__init__.py`  
**Language:** Python  
**Description:** Setup all handlers  
**Last Modified:** 2025-04-02T13:45:22.783540  
**MD5 Hash:** fac9096dbe125eef07aae425b16ce015  

```python
from aiogram import Router
from . import start, pills, reminders, checklist, settings, ads, admin

def setup_routers() -> Router:
    """Setup all handlers"""
    router = Router()
    
    # Include all routers
    router.include_router(start.router)
    router.include_router(pills.router)
    router.include_router(reminders.router)
    router.include_router(checklist.router)
    router.include_router(settings.router)
    router.include_router(ads.router)
    router.include_router(admin.router)
    
    return router

```

### END_FILE:handlers/__init__.py

### BEGIN_FILE:handlers/admin.py

**Path:** `handlers/admin.py`  
**Language:** Python  
**Description:** Handle admin command - only accessible to admins  
**Last Modified:** 2025-04-02T13:45:09.975288  
**MD5 Hash:** 7fd3ff0cbe9e78237296a56c7580b394  

```python
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from database.models import User
from database.db import get_session
from utils.keyboards import get_admin_keyboard, get_admin_users_keyboard
from utils.states import AdminStates
from utils.logger import log_admin_action
from config.config import settings
from services.admin import (
    get_admin_statistics, ban_user, unban_user, 
    extend_subscription, get_admin_logs, export_users_csv
)
import csv
import io

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Handle admin command - only accessible to admins"""
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        return
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            language = "en"
        else:
            language = user.language
    
    # Show admin panel
    await message.answer(
        "Admin panel",
        reply_markup=get_admin_keyboard(language)
    )
    
    log_admin_action(user_id, "opened_admin_panel")

@router.callback_query(F.data == "admin:stats")
async def admin_show_stats(callback: types.CallbackQuery):
    """Show admin statistics"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        language = user.language if user else "en"
    
    # Get statistics
    stats = await get_admin_statistics()
    
    # Format message
    message_text = f"""
📊 Bot Statistics:

👥 Total users: {stats['total_users']}
👤 Active users (7 days): {stats['active_users']}
⭐ Premium users: {stats['premium_users']}
💊 Average medications per user: {stats['avg_pills']}
💰 Monthly income: {stats['monthly_income']} RUB
"""
    
    await callback.message.edit_text(
        message_text,
        reply_markup=get_admin_keyboard(language)
    )
    
    log_admin_action(user_id, "viewed_stats")
    await callback.answer()

@router.callback_query(F.data == "admin:users")
async def admin_manage_users(callback: types.CallbackQuery):
    """Show user management options"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    await callback.message.edit_text(
        "User Management\n\nSelect an action:",
        reply_markup=get_admin_users_keyboard()
    )
    
    log_admin_action(user_id, "opened_user_management")
    await callback.answer()

@router.callback_query(F.data == "admin:ban")
async def admin_ban_user_start(callback: types.CallbackQuery, state: FSMContext):
    """Start ban user process"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    await callback.message.edit_text("Enter the Telegram ID of the user to ban:")
    await state.set_state(AdminStates.waiting_for_user_id)
    await state.update_data(action="ban")
    
    log_admin_action(user_id, "started_ban_process")
    await callback.answer()

@router.callback_query(F.data == "admin:unban")
async def admin_unban_user_start(callback: types.CallbackQuery, state: FSMContext):
    """Start unban user process"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    await callback.message.edit_text("Enter the Telegram ID of the user to unban:")
    await state.set_state(AdminStates.waiting_for_user_id)
    await state.update_data(action="unban")
    
    log_admin_action(user_id, "started_unban_process")
    await callback.answer()

@router.callback_query(F.data == "admin:extend")
async def admin_extend_subscription_start(callback: types.CallbackQuery, state: FSMContext):
    """Start extend subscription process"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    await callback.message.edit_text("Enter the Telegram ID of the user to extend subscription:")
    await state.set_state(AdminStates.waiting_for_user_id)
    await state.update_data(action="extend")
    
    log_admin_action(user_id, "started_extend_subscription_process")
    await callback.answer()

@router.message(AdminStates.waiting_for_user_id)
async def process_user_id_input(message: types.Message, state: FSMContext):
    """Process user ID input for admin actions"""
    admin_id = message.from_user.id
    
    # Check if user is admin
    if admin_id not in settings.ADMIN_IDS:
        return
    
    # Get action from state
    state_data = await state.get_data()
    action = state_data.get("action")
    
    try:
        target_user_id = int(message.text.strip())
    except ValueError:
        await message.answer("Invalid user ID. Please enter a valid numeric ID.")
        return
    
    if action == "ban":
        # Ban user
        success = await ban_user(admin_id, target_user_id)
        
        if success:
            await message.answer(f"User {target_user_id} has been banned.")
            log_admin_action(admin_id, "banned_user", target_user_id)
        else:
            await message.answer(f"User {target_user_id} not found.")
        
        await state.clear()
    
    elif action == "unban":
        # Unban user
        success = await unban_user(admin_id, target_user_id)
        
        if success:
            await message.answer(f"User {target_user_id} has been unbanned.")
            log_admin_action(admin_id, "unbanned_user", target_user_id)
        else:
            await message.answer(f"User {target_user_id} not found.")
        
        await state.clear()
    
    elif action == "extend":
        # Store target user ID and ask for number of days
        await state.update_data(target_user_id=target_user_id)
        await message.answer("Enter the number of days to extend the subscription:")
        await state.set_state(AdminStates.waiting_for_days)
    
    else:
        await state.clear()

@router.message(AdminStates.waiting_for_days)
async def process_days_input(message: types.Message, state: FSMContext):
    """Process days input for subscription extension"""
    admin_id = message.from_user.id
    
    # Check if user is admin
    if admin_id not in settings.ADMIN_IDS:
        return
    
    # Get target user ID from state
    state_data = await state.get_data()
    target_user_id = state_data.get("target_user_id")
    
    try:
        days = int(message.text.strip())
        if days <= 0:
            raise ValueError("Days must be positive")
    except ValueError:
        await message.answer("Invalid input. Please enter a positive number of days.")
        return
    
    # Extend subscription
    success = await extend_subscription(admin_id, target_user_id, days)
    
    if success:
        await message.answer(f"Subscription for user {target_user_id} extended by {days} days.")
        log_admin_action(admin_id, "extended_subscription", target_user_id)
    else:
        await message.answer(f"User {target_user_id} not found.")
    
    await state.clear()

@router.callback_query(F.data == "admin:logs")
async def admin_show_logs(callback: types.CallbackQuery):
    """Show admin logs and reports"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        language = user.language if user else "en"
    
    # Create reports keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Export Users (CSV)", callback_data="admin:export_users")],
        [types.InlineKeyboardButton(text="Back", callback_data="admin:back")]
    ])
    
    await callback.message.edit_text(
        "Logs and Reports\n\nSelect a report to generate:",
        reply_markup=keyboard
    )
    
    log_admin_action(user_id, "opened_logs_and_reports")
    await callback.answer()

@router.callback_query(F.data == "admin:export_users")
async def admin_export_users(callback: types.CallbackQuery):
    """Export users to CSV"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    # Get CSV data
    csv_data = await export_users_csv()
    
    # Create file-like object
    file_obj = io.BytesIO(csv_data.encode('utf-8'))
    file_obj.name = "users_export.csv"
    
    # Send file
    await callback.message.answer_document(
        document=types.BufferedInputFile(
            file_obj.getvalue(),
            filename="users_export.csv"
        )
    )
    
    log_admin_action(user_id, "exported_users_csv")
    await callback.answer()

@router.callback_query(F.data == "admin:back")
async def admin_back_to_main(callback: types.CallbackQuery):
    """Return to admin main menu"""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if user_id not in settings.ADMIN_IDS:
        await callback.answer()
        return
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        language = user.language if user else "en"
    
    await callback.message.edit_text(
        "Admin panel",
        reply_markup=get_admin_keyboard(language)
    )
    
    await callback.answer()

```

### END_FILE:handlers/admin.py

### BEGIN_FILE:handlers/ads.py

**Path:** `handlers/ads.py`  
**Language:** Python  
**Description:** Handle subscription command  
**Last Modified:** 2025-04-02T13:44:55.684151  
**MD5 Hash:** 75e8ff9e4066b0138351634d4b6c068b  

```python
from aiogram import Router, F, types
from aiogram.filters import Command
from sqlalchemy import select
from database.models import User
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_subscription_keyboard
from utils.logger import log_user_action
from services.payments import is_premium_active, get_subscription_invoice
from config.config import settings
from datetime import datetime

router = Router()

@router.message(Command("subscription"))
@router.message(F.text.func(lambda text: text in ["Подписка", "Subscription"]))
async def cmd_subscription(message: types.Message):
    """Handle subscription command"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Check subscription status
        is_premium = await is_premium_active(user)
        
        # Create message based on subscription status
        message_text = get_text("subscription_info", user.language) + "\n\n"
        
        if not is_premium:
            message_text += get_text("free_plan", user.language)
        elif user.premium_until is None:
            message_text += get_text("lifetime_plan", user.language)
        else:
            expiry_date = user.premium_until.strftime("%d.%m.%Y")
            message_text += get_text("premium_plan", user.language, date=expiry_date)
        
        # Add subscription options
        if not (is_premium and user.premium_until is None):  # Don't show options for lifetime subscribers
            message_text += "\n\n" + get_text("subscription_plans", user.language)
            
            await message.answer(
                message_text,
                reply_markup=get_subscription_keyboard(user.language)
            )
        else:
            await message.answer(message_text)
        
        log_user_action(user_id, "viewed_subscription")

@router.callback_query(F.data.startswith("subscribe:"))
async def process_subscription_selection(callback: types.CallbackQuery):
    """Process subscription plan selection"""
    user_id = callback.from_user.id
    plan = callback.data.split(":")[1]  # "subscribe:monthly" -> "monthly"
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get invoice details
        title, description, prices, duration_days = await get_subscription_invoice(plan, user.language)
        
        # Create invoice
        await callback.bot.send_invoice(
            chat_id=user_id,
            title=title,
            description=description,
            payload=f"subscription:{plan}:{duration_days}",
            provider_token=settings.PAYMENT_PROVIDER_TOKEN,
            currency="RUB",
            prices=prices
        )
        
        log_user_action(user_id, "selected_subscription_plan", plan)
        await callback.answer()

@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    """Handle pre-checkout queries"""
    from services.payments import process_pre_checkout
    
    # Validate pre-checkout
    is_valid = await process_pre_checkout(pre_checkout_query)
    
    if is_valid:
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(ok=False, error_message="Payment processing error. Please try again later.")

@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    """Handle successful payment"""
    from services.payments import process_successful_payment
    
    user_id = message.from_user.id
    payment_info = message.successful_payment
    
    # Parse payload
    payload_parts = payment_info.invoice_payload.split(":")
    if len(payload_parts) != 3:
        return
    
    _, subscription_type, duration_days = payload_parts
    duration_days = None if duration_days == "None" else int(duration_days)
    
    # Process payment
    success = await process_successful_payment(
        telegram_id=user_id,
        subscription_type=subscription_type,
        payment_info=payment_info,
        duration_days=duration_days
    )
    
    # Get user's language
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return
        
        language = user.language
    
    # Send confirmation
    if success:
        await message.answer(get_text("payment_success", language))
    else:
        await message.answer(get_text("payment_failed", language))

```

### END_FILE:handlers/ads.py

### BEGIN_FILE:handlers/checklist.py

**Path:** `handlers/checklist.py`  
**Language:** Python  
**Description:** Handle showing today's medication checklist  
**Last Modified:** 2025-04-02T14:58:44.585789  
**MD5 Hash:** 2730be589c0259579e1d087d625662bb  

```python
from aiogram import Router, F, types
from aiogram.filters import Command
from sqlalchemy import select, update
from database.models import User, Medication, Checklist
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_checklist_keyboard
from utils.logger import log_user_action
from datetime import datetime, time
from services.payments import is_premium_active

router = Router()

@router.message(Command("today"))
@router.message(F.text.func(lambda text: text in ["Лекарства на сегодня", "Today's medications"]))
async def cmd_today_checklist(message: types.Message):
    """Handle showing today's medication checklist"""
    user_id = message.from_user.id
    today = datetime.now().date()
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Get user's checklist items for today
        checklist_query = select(Checklist, Medication).join(
            Medication, Checklist.medication_id == Medication.id
        ).where(
            Checklist.user_id == user.id,
            Checklist.date == today
        ).order_by(Medication.time)
        
        result = await session.execute(checklist_query)
        checklist_items = result.all()
        
        if not checklist_items:
            # Если чеклист пуст, попробуем создать его
            medications_query = select(Medication).where(Medication.user_id == user.id)
            medications = (await session.execute(medications_query)).scalars().all()
            
            if medications:
                # Есть лекарства, но нет чеклиста - создаем его
                for medication in medications:
                    new_checklist = Checklist(
                        user_id=user.id,
                        medication_id=medication.id,
                        date=today,
                        status=False
                    )
                    session.add(new_checklist)
                await session.commit()
                
                # Повторно запрашиваем чеклист
                result = await session.execute(checklist_query)
                checklist_items = result.all()
            
            if not checklist_items:
                await message.answer(get_text("no_pills_today", user.language))
                return
        
        # Group medications by schedule (morning, day, evening)
        morning_items = []
        day_items = []
        evening_items = []
        
        for checklist, medication in checklist_items:
            item_time = medication.time
            item_text = get_text(
                "pill_item", 
                user.language,
                name=medication.name,
                time=item_time.strftime("%H:%M")
            )
            
            if medication.schedule == "morning" or (item_time.hour >= 5 and item_time.hour < 12):
                morning_items.append((checklist, item_text))
            elif medication.schedule == "day" or (item_time.hour >= 12 and item_time.hour < 18):
                day_items.append((checklist, item_text))
            else:
                evening_items.append((checklist, item_text))
        
        # Format the checklist message
        today_formatted = today.strftime("%d.%m.%Y")
        message_text = get_text("today_checklist", user.language, date=today_formatted) + "\n\n"
        
        # Add morning section
        if morning_items:
            message_text += get_text("morning_pills", user.language) + "\n"
            for checklist, item_text in morning_items:
                status = "✅ " if checklist.status else ""
                message_text += f"{status}{item_text}\n"
            message_text += "\n"
        
        # Add day section
        if day_items:
            message_text += get_text("day_pills", user.language) + "\n"
            for checklist, item_text in day_items:
                status = "✅ " if checklist.status else ""
                message_text += f"{status}{item_text}\n"
            message_text += "\n"
        
        # Add evening section
        if evening_items:
            message_text += get_text("evening_pills", user.language) + "\n"
            for checklist, item_text in evening_items:
                status = "✅ " if checklist.status else ""
                message_text += f"{status}{item_text}\n"
        
        # Add ad for non-premium users
        is_premium = await is_premium_active(user)
        if not is_premium:
            message_text += "\n" + get_text("ad_banner", user.language)
        
        # Send the checklist
        await message.answer(message_text)
        
        # Send buttons for items that haven't been marked as taken
        for checklist, medication in checklist_items:
            if not checklist.status:
                pill_name = medication.name
                pill_time = medication.time.strftime("%H:%M")
                
                await message.answer(
                    f"{pill_name} - {pill_time}",
                    reply_markup=get_checklist_keyboard(checklist.id, user.language)
                )
        
        log_user_action(user_id, "viewed_today_checklist")

@router.callback_query(F.data.startswith("mark_taken:"))
async def process_mark_as_taken(callback: types.CallbackQuery):
    """Process marking medication as taken"""
    user_id = callback.from_user.id
    checklist_id = int(callback.data.split(":")[1])
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get checklist item
        checklist_query = select(Checklist, Medication).join(
            Medication, Checklist.medication_id == Medication.id
        ).where(
            Checklist.id == checklist_id,
            Checklist.user_id == user.id
        )
        
        result = await session.execute(checklist_query)
        checklist_data = result.first()
        
        if not checklist_data:
            await callback.answer()
            return
        
        checklist, medication = checklist_data
        
        # Mark as taken
        await session.execute(
            update(Checklist)
            .where(Checklist.id == checklist_id)
            .values(status=True)
        )
        
        await session.commit()
        
        # Update message
        await callback.message.edit_text(
            f"✅ {medication.name} - {medication.time.strftime('%H:%M')}"
        )
        
        await callback.answer(
            get_text("marked_as_taken", user.language, name=medication.name)
        )
        
        log_user_action(user_id, "marked_pill_taken", medication.name)


@router.message(Command("update_checklist"))
async def cmd_update_checklist(message: types.Message):
    """Manually update today's checklist"""
    user_id = message.from_user.id
    today = datetime.now().date()
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Get user's medications
        medications_query = select(Medication).where(Medication.user_id == user.id)
        medications = (await session.execute(medications_query)).scalars().all()
        
        if not medications:
            await message.answer(get_text("no_pills_today", user.language))
            return
        
        # Count of new entries
        new_entries = 0
        
        # Create checklist items for each medication
        for medication in medications:
            # Check if checklist item already exists
            checklist_query = select(Checklist).where(
                Checklist.user_id == user.id,
                Checklist.medication_id == medication.id,
                Checklist.date == today
            )
            
            existing_checklist = (await session.execute(checklist_query)).scalar_one_or_none()
            
            if not existing_checklist:
                # Create new checklist item
                new_checklist = Checklist(
                    user_id=user.id,
                    medication_id=medication.id,
                    date=today,
                    status=False
                )
                session.add(new_checklist)
                new_entries += 1
        
        await session.commit()
        
        if new_entries > 0:
            await message.answer(f"Чеклист обновлен. Добавлено {new_entries} новых записей.")
        else:
            await message.answer("Чеклист уже актуален, новых записей не добавлено.")
        
        # Перенаправляем на просмотр чеклиста
        await cmd_today_checklist(message)

```

### END_FILE:handlers/checklist.py

### BEGIN_FILE:handlers/pills.py

**Path:** `handlers/pills.py`  
**Language:** Python  
**Description:** Handle add pill command  
**Last Modified:** 2025-04-03T20:11:47.415617  
**MD5 Hash:** 534ebb62619ffb9959428b3175411b24  

```python
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, func
from database.models import User, Medication
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_schedule_keyboard, get_time_keyboard, get_main_menu_keyboard
from utils.states import AddPillStates
from utils.logger import log_user_action
from datetime import datetime, time
import re
from services.reminders import setup_medication_reminders  # Добавить этот импорт
from aiogram import Bot

router = Router()

@router.message(Command("add_pill"))
@router.message(F.text.func(lambda text: text in ["Добавить лекарство", "Add medication"]))
async def cmd_add_pill(message: types.Message, state: FSMContext):
    """Handle add pill command"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
         # Проверка лимита для обычных пользователей
        if not user.is_premium:
            count_query = (
                select(func.count())
                .select_from(Medication)
                .where(Medication.user_id == user.id)
            )
            med_count = (await session.execute(count_query)).scalar()
            
            if med_count >= 5:
                await message.answer(get_text("limit_reached", user.language))
                return

        # Ask for pill name
        await message.answer(get_text("enter_pill_name", user.language))
        await state.set_state(AddPillStates.waiting_for_name)
        
        # Store user language in state
        await state.update_data(language=user.language)
        
        log_user_action(user_id, "add_pill_command")

@router.message(AddPillStates.waiting_for_name)
async def process_pill_name(message: types.Message, state: FSMContext):
    """Process pill name input"""
    user_id = message.from_user.id
    pill_name = message.text.strip()
    
    if not pill_name:
        return
    
    # Store pill name in state
    await state.update_data(pill_name=pill_name)
    
    # Get user language from state
    state_data = await state.get_data()
    language = state_data.get("language", "en")
    
    # Ask for schedule
    await message.answer(
        get_text("select_schedule", language),
        reply_markup=get_schedule_keyboard(language)
    )
    
    await state.set_state(AddPillStates.waiting_for_schedule)
    
    log_user_action(user_id, "pill_name_entered", pill_name)

@router.callback_query(AddPillStates.waiting_for_schedule, F.data.startswith("schedule:"))
async def process_schedule_selection(callback: types.CallbackQuery, state: FSMContext):
    """Process schedule selection callback"""
    user_id = callback.from_user.id
    selected_schedule = callback.data.split(":")[1]  # "schedule:morning" -> "morning"
    
    # Store schedule in state
    await state.update_data(schedule=selected_schedule)
    
    # Get user language from state
    state_data = await state.get_data()
    language = state_data.get("language", "en")
    
    if selected_schedule == "custom":
        # Ask for custom time
        await callback.message.edit_text(get_text("enter_custom_time", language))
        await state.set_state(AddPillStates.waiting_for_custom_time)
    else:
        # Show time options for selected schedule
        await callback.message.edit_text(
            get_text("select_time", language),
            reply_markup=get_time_keyboard(selected_schedule, language)
        )
        await state.set_state(AddPillStates.waiting_for_time)
    
    log_user_action(user_id, "schedule_selected", selected_schedule)
    await callback.answer()

@router.callback_query(AddPillStates.waiting_for_time, F.data.startswith("time:"))
async def process_time_selection(callback: types.CallbackQuery, state: FSMContext,  bot: Bot):
    """Process time selection callback"""
    user_id = callback.from_user.id
    selected_time = callback.data.split(":")[1] + ":" + callback.data.split(":")[2]  # "time:08:00" -> "08:00"
    # Get state data
    state_data = await state.get_data()
    pill_name = state_data.get("pill_name")
    schedule = state_data.get("schedule")
    language = state_data.get("language", "en")
    
    # Parse time
    hour, minute = map(int, selected_time.split(":"))
    time_obj = time(hour=hour, minute=minute)
    
    # Save pill to database
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        new_medication = Medication(
            user_id=user.id,
            name=pill_name,
            schedule=schedule,
            time=time_obj
        )
        
        session.add(new_medication)
        await session.commit()
    
         # Получаем ID созданного лекарства
        medication_id = new_medication.id
        
        # Создаем запись в чеклисте на сегодня
        from database.models import Checklist
        from datetime import date
        
        today = date.today()
        
        # Проверяем, не существует ли уже такая запись
        checklist_query = select(Checklist).where(
            Checklist.user_id == user.id,
            Checklist.medication_id == medication_id,
            Checklist.date == today
        )
        existing_checklist = (await session.execute(checklist_query)).scalar_one_or_none()
        
        if not existing_checklist:
            # Создаем новую запись в чеклисте
            new_checklist = Checklist(
                user_id=user.id,
                medication_id=medication_id,
                date=today,
                status=False  # Лекарство еще не принято
            )
            session.add(new_checklist)
            await session.commit()

    # Confirm pill addition
    await callback.message.edit_text(
        get_text("pill_added", language, name=pill_name, time=selected_time)
    )
    
    await setup_medication_reminders(bot)
    
    # Clear state
    await state.clear()
    
    log_user_action(user_id, "pill_added", f"{pill_name} at {selected_time}")
    await callback.answer()

@router.message(AddPillStates.waiting_for_custom_time)
async def process_custom_time(message: types.Message, state: FSMContext, bot: Bot):
    """Process custom time input"""
    user_id = message.from_user.id
    time_input = message.text.strip()
    
    # Get state data
    state_data = await state.get_data()
    pill_name = state_data.get("pill_name")
    schedule = state_data.get("schedule")
    language = state_data.get("language", "en")
    
    # Validate time format (HH:MM)
    time_pattern = re.compile(r"^([01]?[0-9]|2[0-3]):([0-5][0-9])$")
    if not time_pattern.match(time_input):
        await message.answer(get_text("invalid_time_format", language))
        return
    
    # Parse time
    hour, minute = map(int, time_input.split(":"))
    time_obj = time(hour=hour, minute=minute)
    
    # Save pill to database
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        new_medication = Medication(
            user_id=user.id,
            name=pill_name,
            schedule="custom",
            time=time_obj
        )
        
        session.add(new_medication)
        await session.commit()

        # Получаем ID созданного лекарства
        medication_id = new_medication.id
        
        # Создаем запись в чеклисте на сегодня
        from database.models import Checklist
        from datetime import date
        
        today = date.today()
        
        # Проверяем, не существует ли уже такая запись
        checklist_query = select(Checklist).where(
            Checklist.user_id == user.id,
            Checklist.medication_id == medication_id,
            Checklist.date == today
        )
        existing_checklist = (await session.execute(checklist_query)).scalar_one_or_none()
        
        if not existing_checklist:
            # Создаем новую запись в чеклисте
            new_checklist = Checklist(
                user_id=user.id,
                medication_id=medication_id,
                date=today,
                status=False  # Лекарство еще не принято
            )
            session.add(new_checklist)
            await session.commit()

    # Confirm pill addition
    await message.answer(
        get_text("pill_added", language, name=pill_name, time=time_input)
    )
    
    await setup_medication_reminders(bot)
    
    # Clear state
    await state.clear()
    
    log_user_action(user_id, "pill_added", f"{pill_name} at {time_input}")


@router.message(Command("my_pills"))
@router.message(F.text.func(lambda text: text in ["Мои лекарства", "My medications"]))
async def cmd_my_pills(message: types.Message):
    """Handle showing user's medications list"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Get user's medications
        medications_query = select(Medication).where(
            Medication.user_id == user.id
        ).order_by(Medication.schedule, Medication.time)
        
        medications = (await session.execute(medications_query)).scalars().all()
        
        if not medications:
            await message.answer(get_text("no_medications", user.language, 
                                         default="You haven't added any medications yet."))
            return
        
        # Format the medications list
        message_text = get_text("your_medications", user.language, 
                               default="Your medications:") + "\n\n"
        
        # Group medications by schedule
        morning_meds = []
        day_meds = []
        evening_meds = []
        custom_meds = []
        
        for med in medications:
            time_str = med.time.strftime("%H:%M")
            med_info = f"{med.name} - {time_str}"
            
            if med.schedule == "morning":
                morning_meds.append((med.id, med_info))
            elif med.schedule == "day":
                day_meds.append((med.id, med_info))
            elif med.schedule == "evening":
                evening_meds.append((med.id, med_info))
            else:  # custom
                custom_meds.append((med.id, med_info))
        
        # Add morning section
        if morning_meds:
            message_text += get_text("morning_pills", user.language) + "\n"
            for med_id, med_info in morning_meds:
                message_text += f"{med_info}\n"
            message_text += "\n"
        
        # Add day section
        if day_meds:
            message_text += get_text("day_pills", user.language) + "\n"
            for med_id, med_info in day_meds:
                message_text += f"{med_info}\n"
            message_text += "\n"
        
        # Add evening section
        if evening_meds:
            message_text += get_text("evening_pills", user.language) + "\n"
            for med_id, med_info in evening_meds:
                message_text += f"{med_info}\n"
            message_text += "\n"
        
        # Add custom section
        if custom_meds:
            message_text += get_text("custom_pills", user.language, 
                                    default="🕒 Custom time:") + "\n"
            for med_id, med_info in custom_meds:
                message_text += f"{med_info}\n"
        
        # Send the medications list
        await message.answer(message_text)
        
        # Create keyboard for medication management
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text=get_text("delete_medication", user.language, default="Delete medication"), 
                callback_data="manage_pills:delete"
            )]
        ])
        
        await message.answer(
            get_text("manage_medications", user.language, default="What would you like to do?"),
            reply_markup=keyboard
        )
        
        log_user_action(user_id, "viewed_medications_list")

@router.callback_query(F.data == "manage_pills:delete")
async def manage_pills_delete(callback: types.CallbackQuery):
    """Handle medication deletion selection"""
    user_id = callback.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get user's medications
        medications_query = select(Medication).where(
            Medication.user_id == user.id
        ).order_by(Medication.name)
        
        medications = (await session.execute(medications_query)).scalars().all()
        
        if not medications:
            await callback.answer(get_text("no_medications", user.language, 
                                         default="You haven't added any medications yet."))
            return
        
        # Create keyboard with all medications
        keyboard_buttons = []
        
        for med in medications:
            time_str = med.time.strftime("%H:%M")
            button_text = f"{med.name} - {time_str}"
            keyboard_buttons.append([types.InlineKeyboardButton(
                text=button_text, 
                callback_data=f"delete_pill:{med.id}"
            )])
        
        # Add cancel button
        keyboard_buttons.append([types.InlineKeyboardButton(
            text=get_text("cancel", user.language, default="Cancel"), 
            callback_data="delete_pill:cancel"
        )])
        
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await callback.message.edit_text(
            get_text("select_medication_to_delete", user.language, 
                    default="Select medication to delete:"),
            reply_markup=keyboard
        )
        
        log_user_action(user_id, "medication_deletion_menu")
        await callback.answer()

@router.callback_query(F.data == "delete_pill:cancel")
async def delete_pill_cancel(callback: types.CallbackQuery):
    """Handle cancellation of medication deletion"""
    user_id = callback.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
    
    await callback.message.edit_text(
        get_text("deletion_cancelled", user.language, 
                default="Operation cancelled.")
    )
    
    log_user_action(user_id, "medication_deletion_cancelled")
    await callback.answer()

@router.callback_query(F.data.startswith("delete_pill:"))
async def delete_pill_confirm(callback: types.CallbackQuery):
    """Handle medication deletion confirmation"""
    user_id = callback.from_user.id
    
    # Skip if it's the cancel button
    if callback.data == "delete_pill:cancel":
        return
    
    # Get medication ID
    medication_id = int(callback.data.split(":")[1])
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get the medication
        medication_query = select(Medication).where(
            Medication.id == medication_id,
            Medication.user_id == user.id
        )
        
        medication = (await session.execute(medication_query)).scalar_one_or_none()
        
        if not medication:
            await callback.answer(get_text("medication_not_found", user.language, 
                                         default="Medication not found."))
            return
        
        # Create confirmation keyboard
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=get_text("confirm_delete", user.language, default="Yes, delete"), 
                    callback_data=f"confirm_delete_pill:{medication_id}"
                ),
                types.InlineKeyboardButton(
                    text=get_text("cancel", user.language, default="Cancel"), 
                    callback_data="delete_pill:cancel"
                )
            ]
        ])
        
        await callback.message.edit_text(
            get_text("confirm_delete_medication", user.language, 
                    default="Are you sure you want to delete {name}?", name=medication.name),
            reply_markup=keyboard
        )
        
        log_user_action(user_id, "medication_deletion_confirmation", medication.name)
        await callback.answer()

@router.callback_query(F.data.startswith("confirm_delete_pill:"))
async def confirm_delete_pill(callback: types.CallbackQuery):
    """Handle final medication deletion"""
    user_id = callback.from_user.id
    
    # Get medication ID
    medication_id = int(callback.data.split(":")[1])
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get the medication
        medication_query = select(Medication).where(
            Medication.id == medication_id,
            Medication.user_id == user.id
        )
        
        medication = (await session.execute(medication_query)).scalar_one_or_none()
        
        if not medication:
            await callback.answer(get_text("medication_not_found", user.language, 
                                         default="Medication not found."))
            return
        
        # Store name for the message
        medication_name = medication.name
        print(medication_name)
        # Delete all related checklist items
        from sqlalchemy import delete
        from database.models import Checklist
        
        delete_checklist = delete(Checklist).where(
            Checklist.medication_id == medication_id
        )
        
        await session.execute(delete_checklist)
        
        # Delete the medication
        await session.delete(medication)
        await session.commit()
        
        await callback.message.edit_text(
            get_text("medication_deleted", user.language, name=medication_name)
        )
        
        log_user_action(user_id, "medication_deleted", medication_name)
        await callback.answer()

```

### END_FILE:handlers/pills.py

### BEGIN_FILE:handlers/reminders.py

**Path:** `handlers/reminders.py`  
**Language:** Python  
**Description:** Process snooze request  
**Last Modified:** 2025-04-02T15:39:30.498152  
**MD5 Hash:** 3db774510bc30a4a4dfc4357462f5aea  

```python
from aiogram import Router, F, types
from aiogram.filters import Command
from sqlalchemy import select, update
from database.models import User, Medication, Checklist, UserSettings
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_snooze_options_keyboard
from utils.logger import log_user_action
from datetime import datetime, timedelta
from services.reminders import setup_daily_reminders
from services.payments import is_premium_active

router = Router()

@router.callback_query(F.data.startswith("snooze:"))
async def process_snooze(callback: types.CallbackQuery):
    """Process snooze request"""
    user_id = callback.from_user.id
    
    # Check if this is a snooze option selection
    parts = callback.data.split(":")
    if len(parts) == 3:
        # This is a snooze time selection
        checklist_id = int(parts[1])
        minutes = int(parts[2])
        
        async with get_session() as session:
            user_query = select(User).where(User.telegram_id == user_id)
            user = (await session.execute(user_query)).scalar_one_or_none()
            
            if not user or user.is_blocked:
                await callback.answer()
                return
            
            # Get the checklist and medication
            checklist_query = select(Checklist, Medication).join(
                Medication, Checklist.medication_id == Medication.id
            ).where(
                Checklist.id == checklist_id,
                Checklist.user_id == user.id
            )
            
            result = await session.execute(checklist_query)
            checklist_data = result.first()
            
            if not checklist_data:
                await callback.answer(get_text("error", user.language, default="Error occurred"))
                return
            
            checklist, medication = checklist_data
            
            # Schedule a one-time reminder
            from apscheduler.triggers.date import DateTrigger
            from services.reminders import scheduler, send_medication_reminder
            
            # Calculate snooze time
            snooze_time = datetime.now() + timedelta(minutes=minutes)
            
            # Create a one-time job for this reminder
            job_id = f"snooze_{checklist.id}_{int(snooze_time.timestamp())}"
            
            scheduler.add_job(
                send_medication_reminder,
                DateTrigger(run_date=snooze_time),
                args=[callback.bot, user_id, medication.id],
                id=job_id,
                replace_existing=True
            )
            
            # Confirm snooze
            await callback.message.edit_text(
                get_text("snoozed_for", user.language, minutes=minutes)
            )
            
            log_user_action(user_id, "snoozed_reminder", f"{medication.name} for {minutes} minutes")
            await callback.answer()
        
    else:
        # This is the initial snooze button press
        checklist_id = int(parts[1])
        
        async with get_session() as session:
            user_query = select(User).where(User.telegram_id == user_id)
            user = (await session.execute(user_query)).scalar_one_or_none()
            
            if not user or user.is_blocked:
                await callback.answer()
                return
            
            # Ask for snooze duration
            await callback.message.edit_text(
                get_text("select_snooze_time", user.language, default="Select snooze time:"),
                reply_markup=get_snooze_options_keyboard(checklist_id, user.language)
            )
            
            await callback.answer()

@router.callback_query(F.data.startswith("disable_reminder:"))
async def disable_reminder(callback: types.CallbackQuery):
    """Disable a specific reminder"""
    user_id = callback.from_user.id
    checklist_id = int(callback.data.split(":")[1])
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Mark the checklist item as taken to prevent further reminders
        await session.execute(
            update(Checklist)
            .where(Checklist.id == checklist_id, Checklist.user_id == user.id)
            .values(status=True)
        )
        
        await session.commit()
        
        # Update the message
        await callback.message.edit_text(
            get_text("reminder_disabled", user.language)
        )
        
        log_user_action(user_id, "disabled_reminder", f"checklist_id: {checklist_id}")
        await callback.answer()

```

### END_FILE:handlers/reminders.py

### BEGIN_FILE:handlers/settings.py

**Path:** `handlers/settings.py`  
**Language:** Python  
**Description:** Handle settings command  
**Last Modified:** 2025-04-02T15:45:00.969663  
**MD5 Hash:** 3d5cd741ddefacdee9ae698167fb0a56  

```python
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, update
from database.models import User
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_language_keyboard, get_main_menu_keyboard, get_settings_keyboard, get_reminder_settings_keyboard
from utils.states import SettingsStates
from utils.logger import log_user_action

router = Router()

@router.message(Command("settings"))
@router.message(F.text.func(lambda text: text in ["Настройки", "Settings"]))
async def cmd_settings(message: types.Message):
    """Handle settings command"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            return
        
        # Send settings menu
        await message.answer(
            get_text("settings", user.language),
            reply_markup=get_settings_keyboard(user.language)
        )
        
        log_user_action(user_id, "opened_settings")

@router.callback_query(F.data == "settings:language")
async def settings_change_language(callback: types.CallbackQuery, state: FSMContext):
    """Handle language change in settings"""
    await callback.message.edit_text(
        get_text("select_language", "en"),
        reply_markup=get_language_keyboard()
    )
    
    await callback.answer()
    
    # Set state to wait for language selection
    await state.set_state(SettingsStates.waiting_for_language)

@router.callback_query(SettingsStates.waiting_for_language, F.data.startswith("language:"))
async def process_settings_language_selection(callback: types.CallbackQuery, state: FSMContext):
    """Process language selection in settings"""
    user_id = callback.from_user.id
    selected_language = callback.data.split(":")[1]  # "language:en" -> "en"
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Update user's language
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(language=selected_language)
        )
        
        await session.commit()
    
    # Send confirmation
    await callback.message.edit_text(
        get_text("language_selected", selected_language)
    )
    
    # Return to main menu with updated language
    await callback.message.answer(
        get_text("main_menu", selected_language),
        reply_markup=get_main_menu_keyboard(selected_language)
    )
    
    # Clear state
    await state.clear()
    
    log_user_action(user_id, "changed_language", selected_language)
    await callback.answer()



@router.callback_query(F.data == "settings:reminders")
async def settings_reminders(callback: types.CallbackQuery):
    """Handle reminder settings"""
    user_id = callback.from_user.id
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get user settings or create if not exists
        from database.models import UserSettings
        
        settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
        user_settings = (await session.execute(settings_query)).scalar_one_or_none()
        
        if not user_settings:
            user_settings = UserSettings(
                user_id=user.id,
                reminders_enabled=True,
                reminder_repeat_minutes=30
            )
            session.add(user_settings)
            await session.commit()
        
        # Create message
        message_text = get_text("reminder_settings", user.language) + "\n\n"
        
        if user_settings.reminders_enabled:
            message_text += get_text("reminders_enabled", user.language)
        else:
            message_text += get_text("reminders_disabled", user.language)
        
        message_text += "\n" + get_text("reminder_repeat_time", user.language) + f" {user_settings.reminder_repeat_minutes} " + get_text("minutes", user.language, default="minutes")
        
        # Send message with settings keyboard
        await callback.message.edit_text(
            message_text,
            reply_markup=get_reminder_settings_keyboard(user.language, user_settings.reminders_enabled)
        )
        
        log_user_action(user_id, "viewed_reminder_settings")
        await callback.answer()

@router.callback_query(F.data.startswith("reminder_settings:"))
async def process_reminder_settings(callback: types.CallbackQuery):
    """Process reminder settings changes"""
    user_id = callback.from_user.id
    action = callback.data.split(":")[1]  # "enable" or "disable"
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get user settings
        from database.models import UserSettings
        
        settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
        user_settings = (await session.execute(settings_query)).scalar_one_or_none()
        
        if not user_settings:
            user_settings = UserSettings(
                user_id=user.id,
                reminders_enabled=True,
                reminder_repeat_minutes=30
            )
            session.add(user_settings)
        
        # Update settings
        if action == "enable":
            user_settings.reminders_enabled = True
        elif action == "disable":
            user_settings.reminders_enabled = False
        
        await session.commit()
        
        # Update message
        message_text = get_text("reminder_settings", user.language) + "\n\n"
        
        if user_settings.reminders_enabled:
            message_text += get_text("reminders_enabled", user.language)
        else:
            message_text += get_text("reminders_disabled", user.language)
        
        message_text += "\n" + get_text("reminder_repeat_time", user.language) + f" {user_settings.reminder_repeat_minutes} " + get_text("minutes", user.language, default="minutes")
        
        # Send message with updated settings keyboard
        await callback.message.edit_text(
            message_text,
            reply_markup=get_reminder_settings_keyboard(user.language, user_settings.reminders_enabled)
        )
        
        log_user_action(user_id, f"reminders_{action}d")
        await callback.answer(get_text("reminder_settings_updated", user.language))

@router.callback_query(F.data.startswith("reminder_repeat:"))
async def process_reminder_repeat(callback: types.CallbackQuery):
    """Process reminder repeat time changes"""
    user_id = callback.from_user.id
    minutes = int(callback.data.split(":")[1])  # 5, 15, or 30
    
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user or user.is_blocked:
            await callback.answer()
            return
        
        # Get user settings
        from database.models import UserSettings
        
        settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
        user_settings = (await session.execute(settings_query)).scalar_one_or_none()
        
        if not user_settings:
            user_settings = UserSettings(
                user_id=user.id,
                reminders_enabled=True,
                reminder_repeat_minutes=minutes
            )
            session.add(user_settings)
        else:
            user_settings.reminder_repeat_minutes = minutes
        
        await session.commit()
        
        # Update message
        message_text = get_text("reminder_settings", user.language) + "\n\n"
        
        if user_settings.reminders_enabled:
            message_text += get_text("reminders_enabled", user.language)
        else:
            message_text += get_text("reminders_disabled", user.language)
        
        message_text += "\n" + get_text("reminder_repeat_time", user.language) + f" {user_settings.reminder_repeat_minutes} " + get_text("minutes", user.language, default="minutes")
        
        # Send message with updated settings keyboard
        await callback.message.edit_text(
            message_text,
            reply_markup=get_reminder_settings_keyboard(user.language, user_settings.reminders_enabled)
        )
        
        log_user_action(user_id, f"reminder_repeat_set_to_{minutes}")
        await callback.answer(get_text("reminder_settings_updated", user.language))

```

### END_FILE:handlers/settings.py

### BEGIN_FILE:handlers/start.py

**Path:** `handlers/start.py`  
**Language:** Python  
**Description:** Handle /start command  
**Last Modified:** 2025-04-03T20:23:34.249914  
**MD5 Hash:** 00cab5ac7ba8d0617536a28a62b3f767  

```python
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from database.models import User
from database.db import get_session
from utils.localization import get_text
from utils.keyboards import get_language_keyboard, get_main_menu_keyboard
from utils.logger import log_user_action
from datetime import datetime, timedelta

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command"""
    user_id = message.from_user.id
    
    async with get_session() as session:
        # Check if user already exists
        user_query = select(User).where(User.telegram_id == user_id)
        existing_user = (await session.execute(user_query)).scalar_one_or_none()
        
        if existing_user:
            # User exists, update last_active
            existing_user.last_active = datetime.utcnow()
            await session.commit()
            
            # Check if user is blocked
            if existing_user.is_blocked:
                await message.answer(get_text("user_blocked", existing_user.language))
                return
            
            premium_status = get_text(
                "premium_status_active" if existing_user.is_premium 
                else "premium_status_inactive", 
                existing_user.language
            )
            
            # Send welcome back message
            await message.answer(
                f"{get_text('welcome', existing_user.language)}\n\n{premium_status}",
                reply_markup=get_main_menu_keyboard(existing_user.language)
            )
            log_user_action(user_id, "start_command", "returning user")
            
        else:
            # New user, ask for language preference
            await message.answer(
                get_text("select_language", "en"),
                reply_markup=get_language_keyboard()
            )
            log_user_action(user_id, "start_command", "new user")

@router.callback_query(F.data.startswith("language:"))
async def process_language_selection(callback: types.CallbackQuery):
    """Process language selection callback"""
    user_id = callback.from_user.id
    selected_language = callback.data.split(":")[1]  # "language:en" -> "en"
    
    async with get_session() as session:
        # Check if user already exists
        user_query = select(User).where(User.telegram_id == user_id)
        existing_user = (await session.execute(user_query)).scalar_one_or_none()
        
        if existing_user:
            # Update existing user's language
            existing_user.language = selected_language
            existing_user.last_active = datetime.utcnow()
        else:
            # Create new user
            new_user = User(
                telegram_id=user_id,
                language=selected_language,
                created_at=datetime.now(),
                last_active=datetime.now(),
                is_premium=True,
                premium_until=datetime.now() + timedelta(days=30)
            )
            session.add(new_user)
        
        await session.commit()

    
    
    welcome_text = (
        f"{get_text('language_selected', selected_language)}\n"
        f"{get_text('trial_activated', selected_language)}")
    
    # Send confirmation and main menu
    await callback.message.edit_text(
        welcome_text
    )
    
    await callback.message.answer(
        get_text("welcome", selected_language),
        reply_markup=get_main_menu_keyboard(selected_language)  
    )
    
    log_user_action(user_id, "language_selected", selected_language)
    await callback.answer()

```

### END_FILE:handlers/start.py

### BEGIN_FILE:migrations/env.py

**Path:** `migrations/env.py`  
**Language:** Python  
**Description:** Run migrations in 'offline' mode.  
**Last Modified:** 2025-04-02T14:07:58.045794  
**MD5 Hash:** 85349ba5de959476592a75a1f100c98b  

```python
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Для миграций используем синхронный URL
from sqlalchemy.ext.asyncio import create_async_engine
from config.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Преобразуем URL из asyncpg в синхронный psycopg2 для миграций
sync_url = settings.database_url.replace("postgresql+asyncpg", "postgresql")
config.set_main_option("sqlalchemy.url", sync_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from database.models import Base
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Используем синхронный URL и синхронный движок для миграций
    from sqlalchemy import create_engine
    
    connectable = create_engine(sync_url)

    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```

### END_FILE:migrations/env.py

### BEGIN_FILE:migrations/versions/5a6c0bb5c0b5_create_tables.py

**Path:** `migrations/versions/5a6c0bb5c0b5_create_tables.py`  
**Language:** Python  
**Description:** create tables  
**Last Modified:** 2025-04-02T14:11:33.623985  
**MD5 Hash:** 59855c8c57f57e9e99b8945553f77d11  

```python
"""create tables

Revision ID: 5a6c0bb5c0b5
Revises: 
Create Date: 2025-04-02 14:11:33.613788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a6c0bb5c0b5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_logs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(length=100), nullable=False),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.Column('is_premium', sa.Boolean(), nullable=True),
    sa.Column('premium_until', sa.DateTime(), nullable=True),
    sa.Column('is_blocked', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_active', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_table('medications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('schedule', sa.String(length=20), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('subscription_type', sa.String(length=20), nullable=False),
    sa.Column('telegram_payment_id', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('checklist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('medication_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['medication_id'], ['medications.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('checklist')
    op.drop_table('payments')
    op.drop_table('medications')
    op.drop_table('users')
    op.drop_table('admin_logs')
    # ### end Alembic commands ###

```

### END_FILE:migrations/versions/5a6c0bb5c0b5_create_tables.py

### BEGIN_FILE:project_analyzer.py

**Path:** `project_analyzer.py`  
**Language:** Python  
**Description:** Enhanced Project Structure Analyzer for AI Readability  
**Last Modified:** 2025-07-21T00:04:25.819842  
**MD5 Hash:** 0808f4b70593265f2f79689b65887254  

```python
#!/usr/bin/env python3
"""
Enhanced Project Structure Analyzer for AI Readability

This script recursively walks through a project directory, analyzes its structure,
and creates a comprehensive output file optimized for both human and AI consumption.
The output is structured in a way that makes it easy for AI systems to understand
the project architecture, file relationships, and code content.
"""

import os
import argparse
import re
import json
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional, Any
import datetime
import hashlib


# Dictionary mapping file extensions to their language/framework
LANGUAGE_EXTENSIONS = {
    # Web/Frontend
    '.html': 'HTML',
    '.htm': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.less': 'Less',
    '.js': 'JavaScript',
    '.jsx': 'React JSX',
    '.ts': 'TypeScript',
    '.tsx': 'React TSX',
    '.vue': 'Vue',
    '.svelte': 'Svelte',
    '.json': 'JSON',
    '.xml': 'XML',
    '.svg': 'SVG',
    
    # Backend
    '.py': 'Python',
    '.php': 'PHP',
    '.rb': 'Ruby',
    '.java': 'Java',
    '.jsp': 'JSP',
    '.asp': 'ASP',
    '.aspx': 'ASP.NET',
    '.cs': 'C#',
    '.vb': 'Visual Basic',
    '.go': 'Go',
    '.rs': 'Rust',
    '.scala': 'Scala',
    '.kt': 'Kotlin',
    '.groovy': 'Groovy',
    '.dart': 'Dart',
    '.swift': 'Swift',
    '.m': 'Objective-C',
    '.mm': 'Objective-C++',
    
    # Systems Programming
    '.c': 'C',
    '.h': 'C Header',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.hpp': 'C++ Header',
    '.asm': 'Assembly',
    
    # Data/ML
    '.sql': 'SQL',
    '.r': 'R',
    '.ipynb': 'Jupyter Notebook',
    
    # Configuration
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.toml': 'TOML',
    '.ini': 'INI',
    '.cfg': 'Config',
    '.conf': 'Config',
    '.env': 'Environment Variables',
    
    # Shell/Scripts
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.ps1': 'PowerShell',
    '.bat': 'Batch',
    '.cmd': 'Command',
    '.awk': 'AWK',
    '.pl': 'Perl',
    '.pm': 'Perl Module',
    
    # Markup/Documentation
    '.md': 'Markdown',
    '.markdown': 'Markdown',
    '.rst': 'reStructuredText',
    '.tex': 'LaTeX',
    
    # Mobile
    '.java': 'Java (Android)',
    '.kt': 'Kotlin (Android)',
    '.swift': 'Swift (iOS)',
    '.m': 'Objective-C (iOS)',
    '.dart': 'Dart (Flutter)',
    
    # Other
    '.lua': 'Lua',
    '.ex': 'Elixir',
    '.exs': 'Elixir Script',
    '.erl': 'Erlang',
    '.hrl': 'Erlang Header',
    '.clj': 'Clojure',
    '.fs': 'F#',
    '.d': 'D',
    '.jl': 'Julia',
    '.hs': 'Haskell',
    '.elm': 'Elm',
    '.coffee': 'CoffeeScript',
}


def get_comment_pattern(file_ext: str) -> List[Tuple[str, str]]:
    """Return the appropriate comment patterns for a given file extension."""
    # Define comment patterns by language type
    single_line_comments = {
        # C-style comments
        'c_style': ['//', '#'],
        # Shell-style comments
        'shell_style': ['#'],
        # SQL-style comments
        'sql_style': ['--'],
        # HTML-style comments
        'html_style': [''],
        # Batch-style comments
        'batch_style': ['REM', '::'],
    }
    
    multi_line_comments = {
        # C-style block comments
        'c_style': [('/*', '*/')],
        # Python/Ruby docstrings
        'py_style': [('"""', '"""'), ("'''", "'''")],
        # HTML comments
        'html_style': [('')],
    }
    
    # Map file extensions to comment styles
    comment_style_map = {
        # C-style single-line comments with C-style block comments
        'c_style_full': ['.js', '.jsx', '.ts', '.tsx', '.c', '.h', '.cpp', '.cc', '.hpp', 
                         '.java', '.cs', '.go', '.swift', '.kt', '.scala', '.php', 
                         '.css', '.scss', '.sass', '.less', '.dart', '.rs', '.m', '.mm'],
        
        # Python-style with both # and docstrings
        'py_style': ['.py', '.rb'],
        
        # Shell script style
        'shell_style': ['.sh', '.bash', '.zsh', '.pl', '.r', '.yaml', '.yml', '.toml'],
        
        # HTML/XML style
        'html_style': ['.html', '.htm', '.xml', '.svg', '.vue', '.svelte', '.jsx', '.tsx'],
        
        # SQL style
        'sql_style': ['.sql'],
        
        # Batch style
        'batch_style': ['.bat', '.cmd'],
    }
    
    patterns = []
    
    # Add single-line comment patterns
    for style, exts in comment_style_map.items():
        if any(file_ext == ext for ext in exts):
            if 'c_style' in style:
                patterns.extend([(p, None) for p in single_line_comments['c_style']])
            if 'shell_style' in style or style == 'py_style':
                patterns.extend([(p, None) for p in single_line_comments['shell_style']])
            if 'sql_style' in style:
                patterns.extend([(p, None) for p in single_line_comments['sql_style']])
            if 'html_style' in style:
                patterns.append((single_line_comments['html_style'][0], single_line_comments['html_style'][1]))
            if 'batch_style' in style:
                patterns.extend([(p, None) for p in single_line_comments['batch_style']])
    
    # Add multi-line comment patterns
    for style, exts in comment_style_map.items():
        if any(file_ext == ext for ext in exts):
            if 'c_style' in style:
                patterns.extend(multi_line_comments['c_style'])
            if style == 'py_style':
                patterns.extend(multi_line_comments['py_style'])
            if 'html_style' in style:
                patterns.extend(multi_line_comments['html_style'])
    
    return patterns


def get_file_description(file_path: Path) -> str:
    """Extract description from a file (docstring, comment, or first line)."""
    try:
        file_ext = file_path.suffix.lower()
        
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            try:
                content = f.read(2000)  # Read first 2000 chars to find description
            except UnicodeDecodeError:
                return "Binary file or encoding error"
            
            if not content.strip():
                return "Empty file"
            
            comment_patterns = get_comment_pattern(file_ext)
            
            # Check for multi-line comments/docstrings
            for start, end in comment_patterns:
                if end:  # This is a multi-line comment pattern
                    pattern = re.escape(start) + r'(.*?)' + re.escape(end)
                    match = re.search(pattern, content, re.DOTALL)
                    if match:
                        desc = match.group(1).strip()
                        lines = desc.split('\n')
                        # Return first non-empty line or first line if all are non-empty
                        for line in lines:
                            if line.strip():
                                return line.strip()
                        return desc
            
            # Check for single-line comments
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                for start, _ in comment_patterns:
                    if not _:  # This is a single-line comment pattern
                        if line.startswith(start):
                            return line[len(start):].strip()
            
            # If no comments found, return the first non-empty line
            for line in lines:
                if line.strip():
                    # Limit line length
                    if len(line.strip()) > 100:
                        return line.strip()[:97] + "..."
                    return line.strip()
            
            return "No description found"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def extract_imports_and_dependencies(file_path: Path, content: str) -> Dict[str, List[str]]:
    """Extract imports and dependencies from a file based on its file type."""
    file_ext = file_path.suffix.lower()
    imports = []
    
    # JavaScript/TypeScript imports
    if file_ext in ['.js', '.jsx', '.ts', '.tsx', '.vue']:
        # ES6 imports
        imports.extend(re.findall(r'import\s+.*?from\s+[\'"](.+?)[\'"]', content))
        # CommonJS requires
        imports.extend(re.findall(r'require\s*$$\s*[\'"](.+?)[\'"]', content))
        
    # Python imports
    elif file_ext == '.py':
        # import statements
        imports.extend(re.findall(r'import\s+(\w+)', content))
        imports.extend(re.findall(r'from\s+(\S+)\s+import', content))
        
    # PHP includes/requires
    elif file_ext == '.php':
        imports.extend(re.findall(r'(include|require|include_once|require_once)\s*\(\s*[\'"](.+?)[\'"]', content))
        imports.extend(re.findall(r'(include|require|include_once|require_once)\s+[\'"](.+?)[\'"]', content))
        
    # Java/C# imports
    elif file_ext in ['.java', '.cs']:
        imports.extend(re.findall(r'import\s+(.+?);', content))
        
    # Ruby requires
    elif file_ext == '.rb':
        imports.extend(re.findall(r'require\s+[\'"](.+?)[\'"]', content))
        
    # Go imports
    elif file_ext == '.go':
        # Find import blocks
        import_blocks = re.findall(r'import\s*\((.*?)$$', content, re.DOTALL)
        for block in import_blocks:
            imports.extend(re.findall(r'[\'"](.+?)[\'"]', block))
        # Find single imports
        imports.extend(re.findall(r'import\s+[\'"](.+?)[\'"]', content))
        
    # C/C++ includes
    elif file_ext in ['.c', '.cpp', '.h', '.hpp']:
        imports.extend(re.findall(r'#include\s+[<"](.+?)[>"]', content))
    
    return {"imports": imports}


def build_directory_tree(path: Path, ignore_dirs: Set[str]) -> Dict[str, Any]:
    """Build a directory tree structure as a nested dictionary."""
    if path.is_file():
        return str(path.name)
    
    result = {}
    try:
        for item in path.iterdir():
            if item.is_dir():
                if item.name in ignore_dirs or item.name.startswith('.'):
                    continue
                result[item.name] = build_directory_tree(item, ignore_dirs)
            else:
                result[item.name] = str(item.name)
    except PermissionError:
        return "Permission Denied"
    
    return result


def collect_file_info(project_dir: Path, ignore_dirs: Set[str], extensions: List[str], 
                     max_file_size: int = 1000000) -> Dict[str, Any]:
    """Collect information about all files in the project."""
    file_info = {}
    
    for root, dirs, files in os.walk(project_dir):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        
        for file in files:
            file_path = Path(root) / file
            rel_path = str(file_path.relative_to(project_dir))
            file_ext = file_path.suffix.lower()
            
            # Skip files that don't match the extensions
            if not any(file_ext == ext.lower() for ext in extensions) and '*' not in extensions:
                continue
            
            # Skip files that are too large
            try:
                if file_path.stat().st_size > max_file_size:
                    file_info[rel_path] = {
                        "path": rel_path,
                        "language": LANGUAGE_EXTENSIONS.get(file_ext, "Unknown"),
                        "size": file_path.stat().st_size,
                        "description": "File too large to process",
                        "content": None,
                        "imports": [],
                        "too_large": True
                    }
                    continue
            except (FileNotFoundError, PermissionError):
                continue
            
            # Get language/framework
            language = LANGUAGE_EXTENSIONS.get(file_ext, "Unknown")
            
            # Get file description
            description = get_file_description(file_path)
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    
                    # Extract imports/dependencies
                    dependencies = extract_imports_and_dependencies(file_path, content)
                    
                    # Add file info to dictionary
                    file_info[rel_path] = {
                        "path": rel_path,
                        "language": language,
                        "size": file_path.stat().st_size,
                        "description": description,
                        "content": content,
                        "imports": dependencies.get("imports", []),
                        "last_modified": datetime.datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        "hash": hashlib.md5(content.encode('utf-8', errors='replace')).hexdigest()
                    }
            except Exception as e:
                file_info[rel_path] = {
                    "path": rel_path,
                    "language": language,
                    "error": str(e),
                    "content": None
                }
    
    return file_info


def write_structured_output(project_dir: Path, output_path: Path, file_info: Dict[str, Any], 
                           directory_tree: Dict[str, Any]) -> None:
    """Write structured output optimized for AI consumption."""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # Write header with metadata
        output_file.write("# PROJECT ANALYSIS DOCUMENT\n\n")
        output_file.write("*This document was automatically generated for AI analysis*\n\n")
        output_file.write(f"**Project Directory:** `{project_dir}`  \n")
        output_file.write(f"**Analysis Date:** {datetime.datetime.now().isoformat()}  \n")
        output_file.write(f"**Total Files Analyzed:** {len(file_info)}  \n\n")
        
        # Write project structure section
        output_file.write("## PROJECT STRUCTURE\n\n")
        output_file.write("```\n")
        output_file.write(json.dumps(directory_tree, indent=2))
        output_file.write("\n```\n\n")
        
        # Write file summary section
        output_file.write("## FILE SUMMARY\n\n")
        output_file.write("| File Path | Language | Size | Description |\n")
        output_file.write("| --- | --- | --- | --- |\n")
        
        for path, info in sorted(file_info.items()):
            size_str = f"{info.get('size', 0) / 1024:.1f} KB" if info.get('size') else "N/A"
            desc = info.get('description', 'No description').replace('|', '\\|').replace('\n', ' ')
            if len(desc) > 50:
                desc = desc[:47] + "..."
            output_file.write(f"| `{path}` | {info.get('language', 'Unknown')} | {size_str} | {desc} |\n")
        
        # Write dependency section
        output_file.write("\n## DEPENDENCIES AND IMPORTS\n\n")
        output_file.write("```json\n")
        dependencies = {}
        for path, info in file_info.items():
            if info.get('imports'):
                dependencies[path] = info.get('imports')
        output_file.write(json.dumps(dependencies, indent=2))
        output_file.write("\n```\n\n")
        
        # Write file contents section with special AI-friendly markers
        output_file.write("## FILE CONTENTS\n\n")
        output_file.write("> Note for AI: Each file is enclosed in a special marker format for easy parsing.\n")
        output_file.write("> BEGIN_FILE:{file_path} and END_FILE:{file_path}\n\n")
        
        for path, info in sorted(file_info.items()):
            if info.get('content') is not None:
                language = info.get('language', 'text').lower()
                output_file.write(f"### BEGIN_FILE:{path}\n\n")
                output_file.write(f"**Path:** `{path}`  \n")
                output_file.write(f"**Language:** {info.get('language', 'Unknown')}  \n")
                output_file.write(f"**Description:** {info.get('description', 'No description')}  \n")
                output_file.write(f"**Last Modified:** {info.get('last_modified', 'Unknown')}  \n")
                output_file.write(f"**MD5 Hash:** {info.get('hash', 'Unknown')}  \n\n")
                
                output_file.write("```" + language + "\n")
                output_file.write(info.get('content', ''))
                output_file.write("\n```\n\n")
                output_file.write(f"### END_FILE:{path}\n\n")
            elif info.get('too_large'):
                output_file.write(f"### FILE:{path} (TOO LARGE)\n\n")
                output_file.write(f"File `{path}` is too large to include in this analysis.\n\n")


def analyze_project(project_dir: Path, output_path: Path, extensions: List[str], 
                   ignore_dirs: Set[str] = None, max_file_size: int = 1000000) -> None:
    """Analyze project structure and create a comprehensive output file optimized for AI."""
    if ignore_dirs is None:
        ignore_dirs = {'.git', 'node_modules', '__pycache__', 'venv', 'env', '.venv', '.env',
                      'dist', 'build', 'target', 'bin', 'obj', '.idea', '.vscode'}
    
    print("Building directory tree...")
    directory_tree = build_directory_tree(project_dir, ignore_dirs)
    
    print("Collecting file information...")
    file_info = collect_file_info(project_dir, ignore_dirs, extensions, max_file_size)
    
    print("Writing structured output...")
    write_structured_output(project_dir, output_path, file_info, directory_tree)


def main():
    parser = argparse.ArgumentParser(description='Analyze project structure and create an AI-optimized output file.')
    parser.add_argument('--dir', '-d', type=str, default='.', 
                        help='Project directory path (default: current directory)')
    parser.add_argument('--output', '-o', type=str, default='project_analysis.md',
                        help='Output file path (default: project_analysis.md)')
    parser.add_argument('--extensions', '-e', type=str, default='*',
                        help='Comma-separated list of file extensions to include (default: all code files)')
    parser.add_argument('--ignore', '-i', type=str, 
                        default='.git,node_modules,__pycache__,venv,env,.venv,.env,dist,build,target,bin,obj,.idea,.vscode',
                        help='Comma-separated list of directories to ignore')
    parser.add_argument('--max-size', '-m', type=int, default=1000000,
                        help='Maximum file size in bytes to include (default: 1MB)')
    
    args = parser.parse_args()
    
    project_dir = Path(args.dir).resolve()
    output_path = Path(args.output)
    
    # Handle extensions
    if args.extensions == '*':
        extensions = list(LANGUAGE_EXTENSIONS.keys())
    else:
        extensions = args.extensions.split(',')
        # Ensure all extensions start with a dot
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    
    ignore_dirs = set(args.ignore.split(','))
    max_file_size = args.max_size
    
    print(f"Analyzing project: {project_dir}")
    print(f"Output file: {output_path}")
    print(f"File extensions: {extensions if args.extensions != '*' else 'All code files'}")
    print(f"Ignored directories: {ignore_dirs}")
    print(f"Maximum file size: {max_file_size} bytes")
    
    analyze_project(project_dir, output_path, extensions, ignore_dirs, max_file_size)
    
    print(f"Analysis complete. Results saved to {output_path}")


if __name__ == "__main__":
    main()

```

### END_FILE:project_analyzer.py

### BEGIN_FILE:services/__init__.py

**Path:** `services/__init__.py`  
**Language:** Python  
**Description:** Empty file  
**Last Modified:** 2025-04-02T13:40:25.063085  
**MD5 Hash:** d41d8cd98f00b204e9800998ecf8427e  

```python

```

### END_FILE:services/__init__.py

### BEGIN_FILE:services/admin.py

**Path:** `services/admin.py`  
**Language:** Python  
**Description:** Get statistics for admin panel  
**Last Modified:** 2025-04-02T13:44:06.047405  
**MD5 Hash:** 991daad4d158e7436aca6c6e9a30ebdb  

```python
from datetime import datetime, timedelta
from sqlalchemy import select, func, update, desc
from database.models import User, Medication, Checklist, Payment, AdminLog
from database.db import get_session
from utils.logger import log_admin_action

async def get_admin_statistics() -> dict:
    """Get statistics for admin panel"""
    async with get_session() as session:
        # Total users count
        total_users_query = select(func.count()).select_from(User)
        total_users = (await session.execute(total_users_query)).scalar()
        
        # Active users in last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_users_query = select(func.count()).select_from(User).where(
            User.last_active >= seven_days_ago
        )
        active_users = (await session.execute(active_users_query)).scalar()
        
        # Premium users count
        premium_users_query = select(func.count()).select_from(User).where(
            User.is_premium == True
        )
        premium_users = (await session.execute(premium_users_query)).scalar()
        
        # Average medications per user
        avg_pills_query = select(func.avg(
            select(func.count())
            .select_from(Medication)
            .where(Medication.user_id == User.id)
            .correlate(User)
            .scalar_subquery()
        )).select_from(User)
        avg_pills = (await session.execute(avg_pills_query)).scalar() or 0
        avg_pills = round(avg_pills, 2)
        
        # Monthly income (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        income_query = select(func.sum(Payment.amount)).where(
            Payment.created_at >= thirty_days_ago,
            Payment.status == "completed"
        )
        monthly_income = (await session.execute(income_query)).scalar() or 0
        monthly_income = monthly_income / 100  # Convert from kopecks to rubles
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "premium_users": premium_users,
            "avg_pills": avg_pills,
            "monthly_income": monthly_income
        }

async def ban_user(admin_id: int, user_telegram_id: int) -> bool:
    """Ban a user"""
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_telegram_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return False
        
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_blocked=True)
        )
        
        # Log admin action
        admin_log = AdminLog(
            admin_id=admin_id,
            action="ban_user",
            details=f"Banned user with telegram_id {user_telegram_id}"
        )
        session.add(admin_log)
        
        await session.commit()
        
        log_admin_action(admin_id, "ban_user", user_telegram_id)
        return True

async def unban_user(admin_id: int, user_telegram_id: int) -> bool:
    """Unban a user"""
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_telegram_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return False
        
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_blocked=False)
        )
        
        # Log admin action
        admin_log = AdminLog(
            admin_id=admin_id,
            action="unban_user",
            details=f"Unbanned user with telegram_id {user_telegram_id}"
        )
        session.add(admin_log)
        
        await session.commit()
        
        log_admin_action(admin_id, "unban_user", user_telegram_id)
        return True

async def extend_subscription(admin_id: int, user_telegram_id: int, days: int) -> bool:
    """Extend user subscription"""
    async with get_session() as session:
        user_query = select(User).where(User.telegram_id == user_telegram_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return False
        
        # Calculate new premium_until date
        if user.is_premium and user.premium_until and user.premium_until > datetime.utcnow():
            new_premium_until = user.premium_until + timedelta(days=days)
        else:
            new_premium_until = datetime.utcnow() + timedelta(days=days)
        
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_premium=True, premium_until=new_premium_until)
        )
        
        # Log admin action
        admin_log = AdminLog(
            admin_id=admin_id,
            action="extend_subscription",
            details=f"Extended subscription for user {user_telegram_id} by {days} days"
        )
        session.add(admin_log)
        
        await session.commit()
        
        log_admin_action(admin_id, "extend_subscription", user_telegram_id)
        return True

async def get_admin_logs(limit: int = 50) -> list:
    """Get recent admin logs"""
    async with get_session() as session:
        logs_query = select(AdminLog).order_by(desc(AdminLog.created_at)).limit(limit)
        logs = (await session.execute(logs_query)).scalars().all()
        return logs

async def export_users_csv() -> str:
    """Export users data to CSV"""
    async with get_session() as session:
        users_query = select(User)
        users = (await session.execute(users_query)).scalars().all()
        
        csv_data = "id,telegram_id,language,is_premium,premium_until,is_blocked,created_at,last_active\n"
        
        for user in users:
            premium_until = user.premium_until.strftime("%Y-%m-%d %H:%M:%S") if user.premium_until else "N/A"
            created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
            last_active = user.last_active.strftime("%Y-%m-%d %H:%M:%S")
            
            csv_data += f"{user.id},{user.telegram_id},{user.language},{user.is_premium},{premium_until},"
            csv_data += f"{user.is_blocked},{created_at},{last_active}\n"
        
        return csv_data

```

### END_FILE:services/admin.py

### BEGIN_FILE:services/payments.py

**Path:** `services/payments.py`  
**Language:** Python  
**Description:** Check if user has an active premium subscription  
**Last Modified:** 2025-04-03T20:29:20.200582  
**MD5 Hash:** 24f43f8cdbbc573d486d3d29b182ad33  

```python
from datetime import datetime, timedelta
from sqlalchemy import select, update
from database.models import User, Payment
from database.db import get_session
from config.config import settings
from utils.logger import log_payment
from aiogram.types import LabeledPrice, PreCheckoutQuery

async def is_premium_active(user: User) -> bool:
    """Check if user has an active premium subscription"""
    if not user.is_premium:
        return False
    
    # Lifetime subscription
    if user.premium_until is None:
        return True
    
    # Subscription with expiration date
    return datetime.utcnow() < user.premium_until

async def get_subscription_invoice(subscription_type: str, user_language: str) -> tuple:
    """Get invoice data for subscription purchase"""
    if subscription_type == "monthly":
        title = "Monthly Premium Subscription" if user_language == "en" else "Месячная премиум-подписка"
        description = "Remove ads and support the app for one month" if user_language == "en" else "Отключение рекламы и поддержка приложения на один месяц"
        price = settings.MONTHLY_PRICE
        duration_days = 30
    elif subscription_type == "yearly":
        title = "Yearly Premium Subscription" if user_language == "en" else "Годовая премиум-подписка"
        description = "Remove ads and support the app for one year" if user_language == "en" else "Отключение рекламы и поддержка приложения на один год"
        price = settings.YEARLY_PRICE
        duration_days = 365
    elif subscription_type == "lifetime":
        title = "Lifetime Premium Subscription" if user_language == "en" else "Бессрочная премиум-подписка"
        description = "Remove ads forever and support the app" if user_language == "en" else "Отключение рекламы навсегда и поддержка приложения"
        price = settings.LIFETIME_PRICE
        duration_days = None
    else:
        raise ValueError(f"Invalid subscription type: {subscription_type}")
    
    prices = [LabeledPrice(label=title, amount=price)]
    
    return title, description, prices, duration_days

async def process_successful_payment(telegram_id: int, subscription_type: str, payment_info, duration_days: int = None):
    """Process successful payment and update user subscription"""
    async with get_session() as session:
        # Get user
        user_query = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            return False
        
        # Calculate new subscription end date
        if duration_days is None:  # Lifetime subscription
            new_premium_until = None
        else:
            # If user already has active subscription, extend it
            if user.is_premium and user.premium_until and user.premium_until > datetime.utcnow():
                new_premium_until = user.premium_until + timedelta(days=duration_days)
            else:
                new_premium_until = datetime.utcnow() + timedelta(days=duration_days)
        
        # Update user subscription
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_premium=True, premium_until=new_premium_until)
        )
        
        # Record payment
        amount = payment_info.total_amount
        telegram_payment_id = payment_info.telegram_payment_charge_id
        
        new_payment = Payment(
            user_id=user.id,
            amount=amount,
            subscription_type=subscription_type,
            telegram_payment_id=telegram_payment_id,
            status="completed"
        )
        
        session.add(new_payment)
        await session.commit()
        
        # Log payment
        log_payment(
            user_id=telegram_id,
            amount=amount / 100,  # Convert from kopecks to rubles
            plan=subscription_type,
            status="completed"
        )
        
        return True

async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery) -> bool:
    """Process pre-checkout query and validate payment"""
    # Here you could add additional validation if needed
    return True
    
```

### END_FILE:services/payments.py

### BEGIN_FILE:services/reminders.py

**Path:** `services/reminders.py`  
**Language:** Python  
**Description:** Setup daily reminder jobs  
**Last Modified:** 2025-04-02T15:41:22.840565  
**MD5 Hash:** 3234ab37493decbfc6020eb65c279abe  

```python
from datetime import datetime, timedelta
from sqlalchemy import select, and_
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.models import User, Medication, Checklist
from database.db import get_session
from aiogram import Bot
from utils.localization import get_text
from utils.keyboards import get_checklist_keyboard, get_subscription_keyboard, get_reminder_action_keyboard
from utils.logger import log_info, log_error
from config.config import settings
from services.payments import is_premium_active
import asyncio

scheduler = AsyncIOScheduler()

async def setup_daily_reminders(bot: Bot):
    """Setup daily reminder jobs"""
    log_info("Setting up daily reminder jobs")
    
    # Clear existing jobs
    scheduler.remove_all_jobs()
    
    # Add job to generate daily checklists
    scheduler.add_job(
        generate_daily_checklists,
        CronTrigger(hour=0, minute=1),  # Run at 00:01 every day
        args=[bot],
        id="generate_checklists"
    )
    
    # Add job to check for expiring subscriptions
    scheduler.add_job(
        check_expiring_subscriptions,
        CronTrigger(hour=12, minute=0),  # Run at 12:00 every day
        args=[bot],
        id="check_subscriptions"
    )
    
    # Setup individual reminder jobs for each user's medications
    await setup_medication_reminders(bot)
    
    # Start the scheduler
    if not scheduler.running:
        scheduler.start()

async def setup_medication_reminders(bot: Bot):
    """Setup reminder jobs for all users' medications"""
    log_info("Setting up medication reminders")
    
    async with get_session() as session:
        # Get all active users and their medications
        query = select(User, Medication).join(
            Medication, User.id == Medication.user_id
        ).where(User.is_blocked == False)
        
        result = await session.execute(query)
        
        for user, medication in result:
            hour = medication.time.hour
            minute = medication.time.minute
            
            job_id = f"reminder_{medication.id}"
            
            # Remove existing job if it exists
            if scheduler.get_job(job_id):
                scheduler.remove_job(job_id)
            
            # Add new reminder job
            scheduler.add_job(
                send_medication_reminder,
                CronTrigger(hour=hour, minute=minute),
                args=[bot, user.telegram_id, medication.id],
                id=job_id
            )
            
            # Add follow-up reminder if needed
            followup_job_id = f"followup_{medication.id}"
            if scheduler.get_job(followup_job_id):
                scheduler.remove_job(followup_job_id)
                
            followup_hour = hour
            followup_minute = minute + settings.REMINDER_RETRY_MINUTES
            
            if followup_minute >= 60:
                followup_hour = (hour + followup_minute // 60) % 24
                followup_minute = followup_minute % 60
            
            scheduler.add_job(
                send_followup_reminder,
                CronTrigger(hour=followup_hour, minute=followup_minute),
                args=[bot, user.telegram_id, medication.id],
                id=followup_job_id
            )

async def generate_daily_checklists(bot: Bot):
    """Generate daily checklists for all users"""
    log_info("Generating daily checklists")
    today = datetime.now().date()
    
    async with get_session() as session:
        # Get all active users and their medications
        query = select(User, Medication).join(
            Medication, User.id == Medication.user_id
        ).where(User.is_blocked == False)
        
        result = await session.execute(query)
        user_medications = {}
        
        for user, medication in result:
            if user.id not in user_medications:
                user_medications[user.id] = []
            user_medications[user.id].append(medication)
        
        # Create checklist items for each user's medications
        for user_id, medications in user_medications.items():
            for medication in medications:
                # Check if checklist item already exists
                checklist_query = select(Checklist).where(
                    Checklist.user_id == user_id,
                    Checklist.medication_id == medication.id,
                    Checklist.date == today
                )
                
                checklist_exists = await session.execute(checklist_query)
                if checklist_exists.first() is None:  # Исправлено условие проверки
                    # Create new checklist item
                    new_checklist = Checklist(
                        user_id=user_id,
                        medication_id=medication.id,
                        date=today,
                        status=False
                    )
                    session.add(new_checklist)
        
        await session.commit()


async def send_medication_reminder(bot: Bot, telegram_id: int, medication_id: int):
    """Send a reminder to take medication"""
    try:
        async with get_session() as session:
            # Get user and medication info
            user_query = select(User).where(User.telegram_id == telegram_id)
            user = (await session.execute(user_query)).scalar_one_or_none()
            
            if not user or user.is_blocked:
                return
            
            # Check if reminders are enabled for this user
            from database.models import UserSettings
            
            settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
            user_settings = (await session.execute(settings_query)).scalar_one_or_none()
            
            # If user has settings and reminders are disabled, don't send reminder
            if user_settings and not user_settings.reminders_enabled:
                return
            
            medication_query = select(Medication).where(Medication.id == medication_id)
            medication = (await session.execute(medication_query)).scalar_one_or_none()
            
            if not medication:
                return
            
            # Get today's checklist item
            today = datetime.now().date()
            checklist_query = select(Checklist).where(
                Checklist.user_id == user.id,
                Checklist.medication_id == medication_id,
                Checklist.date == today
            )
            
            checklist = (await session.execute(checklist_query)).scalar_one_or_none()
            
            # If already taken, don't send reminder
            if checklist and checklist.status:
                return
            
            # Create checklist item if it doesn't exist
            if not checklist:
                checklist = Checklist(
                    user_id=user.id,
                    medication_id=medication_id,
                    date=today,
                    status=False
                )
                session.add(checklist)
                await session.commit()
                checklist_id = checklist.id
            else:
                checklist_id = checklist.id
            
            # Send reminder message
            reminder_text = get_text("reminder", user.language, name=medication.name)
            
            # Add ad banner for non-premium users
            is_premium = await is_premium_active(user)
            if not is_premium:
                ad_text = "\n\n" + get_text("ad_banner", user.language)
                reminder_text += ad_text
            
            await bot.send_message(
                chat_id=telegram_id,
                text=reminder_text,
                reply_markup=get_reminder_action_keyboard(checklist_id, user.language)
            )
    
    except Exception as e:
        log_error(f"Error sending reminder: {e}", exc_info=e)

async def send_followup_reminder(bot: Bot, telegram_id: int, medication_id: int):
    """Send a follow-up reminder if medication hasn't been marked as taken"""
    try:
        async with get_session() as session:
            # Get user and medication info
            user_query = select(User).where(User.telegram_id == telegram_id)
            user = (await session.execute(user_query)).scalar_one_or_none()
            
            if not user or user.is_blocked:
                return
            
            # Check if reminders are enabled for this user
            from database.models import UserSettings
            
            settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
            user_settings = (await session.execute(settings_query)).scalar_one_or_none()
            
            # If user has settings and reminders are disabled, don't send reminder
            if user_settings and not user_settings.reminders_enabled:
                return
            
            medication_query = select(Medication).where(Medication.id == medication_id)
            medication = (await session.execute(medication_query)).scalar_one_or_none()
            
            if not medication:
                return
            
            # Get today's checklist item
            today = datetime.now().date()
            checklist_query = select(Checklist).where(
                Checklist.user_id == user.id,
                Checklist.medication_id == medication_id,
                Checklist.date == today
            )
            
            checklist = (await session.execute(checklist_query)).scalar_one_or_none()
            
            # If already taken or checklist doesn't exist, don't send reminder
            if not checklist or checklist.status:
                return
            
            # Send follow-up reminder message
            reminder_text = get_text("reminder_repeat", user.language, name=medication.name)
            
            # Add ad banner for non-premium users
            is_premium = await is_premium_active(user)
            if not is_premium:
                ad_text = "\n\n" + get_text("ad_banner", user.language)
                reminder_text += ad_text
            
            await bot.send_message(
                chat_id=telegram_id,
                text=reminder_text,
                reply_markup=get_reminder_action_keyboard(checklist.id, user.language)
            )
    
    except Exception as e:
        log_error(f"Error sending follow-up reminder: {e}", exc_info=e)

async def setup_medication_reminders(bot: Bot):
    """Setup reminder jobs for all users' medications"""
    log_info("Setting up medication reminders")
    
    async with get_session() as session:
        # Get all active users and their medications
        query = select(User, Medication).join(
            Medication, User.id == Medication.user_id
        ).where(User.is_blocked == False)
        
        result = await session.execute(query)
        
        for user, medication in result:
            hour = medication.time.hour
            minute = medication.time.minute
            
            job_id = f"reminder_{medication.id}"
            
            # Remove existing job if it exists
            if scheduler.get_job(job_id):
                scheduler.remove_job(job_id)
            
            # Add new reminder job
            scheduler.add_job(
                send_medication_reminder,
                CronTrigger(hour=hour, minute=minute),
                args=[bot, user.telegram_id, medication.id],
                id=job_id
            )
            
            # Get user settings
            from database.models import UserSettings
            
            settings_query = select(UserSettings).where(UserSettings.user_id == user.id)
            user_settings = (await session.execute(settings_query)).scalar_one_or_none()
            
            # Default repeat time
            repeat_minutes = 30
            
            if user_settings:
                repeat_minutes = user_settings.reminder_repeat_minutes
            
            # Add follow-up reminder if needed
            followup_job_id = f"followup_{medication.id}"
            if scheduler.get_job(followup_job_id):
                scheduler.remove_job(followup_job_id)
                
            followup_hour = hour
            followup_minute = minute + repeat_minutes
            
            if followup_minute >= 60:
                followup_hour = (hour + followup_minute // 60) % 24
                followup_minute = followup_minute % 60
            
            scheduler.add_job(
                send_followup_reminder,
                CronTrigger(hour=followup_hour, minute=followup_minute),
                args=[bot, user.telegram_id, medication.id],
                id=followup_job_id
            )

async def check_expiring_subscriptions(bot: Bot):
    """Check for subscriptions expiring tomorrow and send notifications"""
    log_info("Checking for expiring subscriptions")
    tomorrow = datetime.now().date() + timedelta(days=1)
    tomorrow_start = datetime.combine(tomorrow, datetime.min.time())
    tomorrow_end = datetime.combine(tomorrow, datetime.max.time())
    
    async with get_session() as session:
        # Find users with subscriptions expiring tomorrow
        query = select(User).where(
            and_(
                User.is_premium == True,
                User.premium_until >= tomorrow_start,
                User.premium_until <= tomorrow_end
            )
        )
        
        result = await session.execute(query)
        expiring_users = result.scalars().all()
        
        for user in expiring_users:
            # Send expiration notification
            notification_text = get_text("subscription_expiring", user.language)
            
            await bot.send_message(
                chat_id=user.telegram_id,
                text=notification_text,
                reply_markup=get_subscription_keyboard(user.language)
            )

```

### END_FILE:services/reminders.py

### BEGIN_FILE:utils/__init__.py

**Path:** `utils/__init__.py`  
**Language:** Python  
**Description:** Empty file  
**Last Modified:** 2025-04-02T13:40:25.068085  
**MD5 Hash:** d41d8cd98f00b204e9800998ecf8427e  

```python

```

### END_FILE:utils/__init__.py

### BEGIN_FILE:utils/keyboards.py

**Path:** `utils/keyboards.py`  
**Language:** Python  
**Description:** Get keyboard for settings menu  
**Last Modified:** 2025-04-02T15:43:14.229045  
**MD5 Hash:** ebd8f661f20000a9eff7cc792be536d6  

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.localization import get_text
from datetime import datetime, time


def get_language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language:ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="language:en")
    )
    return builder.as_markup()


def get_settings_keyboard(language: str) -> InlineKeyboardMarkup:
    """Get keyboard for settings menu"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text="🌐 " + get_text("change_language", language, default="Change language"),
            callback_data="settings:language"
        ),
        InlineKeyboardButton(
            text="⏰ " + get_text("reminder_settings", language),
            callback_data="settings:reminders"
        )
    )
    
    builder.adjust(1)
    return builder.as_markup()

def get_main_menu_keyboard(language: str) -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=get_text("add_pill", language))],
        [KeyboardButton(text=get_text("today_pills", language)), KeyboardButton(text=get_text("my_medications", language))],
        [KeyboardButton(text=get_text("settings", language)), KeyboardButton(text=get_text("subscription", language))]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_schedule_keyboard(language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=get_text("morning", language), callback_data="schedule:morning"),
        InlineKeyboardButton(text=get_text("day", language), callback_data="schedule:day"),
        InlineKeyboardButton(text=get_text("evening", language), callback_data="schedule:evening"),
        InlineKeyboardButton(text=get_text("custom_time", language), callback_data="schedule:custom")
    )
    builder.adjust(2)
    return builder.as_markup()

def get_time_keyboard(schedule: str, language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if schedule == "morning":
        times = ["06:00", "07:00", "08:00", "09:00"]
    elif schedule == "day":
        times = ["12:00", "13:00", "14:00", "15:00"]
    elif schedule == "evening":
        times = ["18:00", "19:00", "20:00", "21:00"]
    else:
        return InlineKeyboardMarkup()
    
    for t in times:
        builder.add(InlineKeyboardButton(text=t, callback_data=f"time:{t}"))
    
    builder.adjust(2)
    return builder.as_markup()

def get_checklist_keyboard(pill_id: int, language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=get_text("mark_as_taken", language),
            callback_data=f"mark_taken:{pill_id}"
        )
    )
    return builder.as_markup()

def get_subscription_keyboard(language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=get_text("monthly_plan", language), callback_data="subscribe:monthly"),
        InlineKeyboardButton(text=get_text("yearly_plan", language), callback_data="subscribe:yearly"),
        InlineKeyboardButton(text=get_text("lifetime_plan_purchase", language), callback_data="subscribe:lifetime")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_admin_keyboard(language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=get_text("admin_stats", language), callback_data="admin:stats"),
        InlineKeyboardButton(text=get_text("admin_users", language), callback_data="admin:users"),
        InlineKeyboardButton(text=get_text("admin_logs", language), callback_data="admin:logs")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_admin_users_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Ban User", callback_data="admin:ban"),
        InlineKeyboardButton(text="Unban User", callback_data="admin:unban"),
        InlineKeyboardButton(text="Extend Subscription", callback_data="admin:extend")
    )
    builder.adjust(1)
    return builder.as_markup()


def get_reminder_settings_keyboard(language: str, reminders_enabled: bool) -> InlineKeyboardMarkup:
    """Get keyboard for reminder settings"""
    builder = InlineKeyboardBuilder()
    
    if reminders_enabled:
        builder.add(InlineKeyboardButton(
            text=get_text("disable_reminders", language),
            callback_data="reminder_settings:disable"
        ))
    else:
        builder.add(InlineKeyboardButton(
            text=get_text("enable_reminders", language),
            callback_data="reminder_settings:enable"
        ))
    
    builder.add(
        InlineKeyboardButton(
            text=get_text("5_minutes", language),
            callback_data="reminder_repeat:5"
        ),
        InlineKeyboardButton(
            text=get_text("15_minutes", language),
            callback_data="reminder_repeat:15"
        ),
        InlineKeyboardButton(
            text=get_text("30_minutes", language),
            callback_data="reminder_repeat:30"
        )
    )
    
    builder.adjust(1, 3)
    return builder.as_markup()

def get_reminder_action_keyboard(checklist_id: int, language: str) -> InlineKeyboardMarkup:
    """Get keyboard for reminder actions"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text=get_text("take_now", language),
            callback_data=f"mark_taken:{checklist_id}"
        ),
        InlineKeyboardButton(
            text=get_text("snooze", language),
            callback_data=f"snooze:{checklist_id}"
        ),
        InlineKeyboardButton(
            text=get_text("disable_this_reminder", language),
            callback_data=f"disable_reminder:{checklist_id}"
        )
    )
    
    builder.adjust(2, 1)
    return builder.as_markup()

def get_snooze_options_keyboard(checklist_id: int, language: str) -> InlineKeyboardMarkup:
    """Get keyboard for snooze options"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text=get_text("5_minutes", language),
            callback_data=f"snooze:{checklist_id}:5"
        ),
        InlineKeyboardButton(
            text=get_text("15_minutes", language),
            callback_data=f"snooze:{checklist_id}:15"
        ),
        InlineKeyboardButton(
            text=get_text("30_minutes", language),
            callback_data=f"snooze:{checklist_id}:30"
        )
    )
    
    builder.adjust(3)
    return builder.as_markup()

```

### END_FILE:utils/keyboards.py

### BEGIN_FILE:utils/localization.py

**Path:** `utils/localization.py`  
**Language:** Python  
**Description:** from typing import Dict, Any  
**Last Modified:** 2025-04-03T20:20:11.660600  
**MD5 Hash:** 9f8ab44ed01d2380da137b43e1fea8af  

```python
from typing import Dict, Any

TEXTS = {
    "ru": {
        "welcome": "Добро пожаловать в МедНапоминалку! Я буду помогать вам не забывать принимать лекарства вовремя.",
        "language_selected": "Вы выбрали русский язык.",
        "select_language": "Выберите язык / Select language:",
        "main_menu": "Главное меню:",
        "add_pill": "Добавить лекарство",
        "today_pills": "Лекарства на сегодня",
        "settings": "Настройки",
        "subscription": "Подписка",
        "enter_pill_name": "Введите название лекарства:",
        "select_schedule": "Выберите режим приёма:",
        "morning": "Утро",
        "day": "День",
        "evening": "Вечер",
        "custom_time": "Своё время",
        "select_time": "Выберите время приёма:",
        "enter_custom_time": "Введите своё время в формате ЧЧ:ММ (например, 08:30):",
        "invalid_time_format": "Неверный формат времени. Пожалуйста, используйте формат ЧЧ:ММ (например, 08:30).",
        "pill_added": "Лекарство {name} добавлено на {time}",
        "no_pills_today": "На сегодня нет запланированных лекарств.",
        "today_checklist": "Ваш чек-лист на сегодня ({date}):",
        "morning_pills": "🌅 Утро:",
        "day_pills": "☀️ День:",
        "evening_pills": "🌙 Вечер:",
        "pill_item": "{name} - {time}",
        "mark_as_taken": "✅ Принято",
        "marked_as_taken": "Отмечено как принято: {name}",
        "reminder": "Напоминание: Пора принять {name}!",
        "reminder_repeat": "Напоминаю: Вы ещё не отметили приём лекарства {name}!",
        "subscription_info": "Информация о подписке:",
        "free_plan": "У вас бесплатный план. Реклама отображается в напоминаниях.",
        "premium_plan": "У вас премиум-подписка до {date}.",
        "lifetime_plan": "У вас бессрочная премиум-подписка.",
        "subscription_plans": "Планы подписки:",
        "monthly_plan": "Месячная - 99₽",
        "yearly_plan": "Годовая - 799₽",
        "lifetime_plan_purchase": "Бессрочная - 1999₽",
        "subscription_expiring": "Ваша подписка истекает завтра. Желаете продлить?",
        "subscription_expired": "Ваша подписка истекла. Теперь вы используете бесплатный план с рекламой.",
        "payment_success": "Оплата прошла успешно! Ваша подписка активирована.",
        "payment_failed": "Произошла ошибка при оплате. Пожалуйста, попробуйте снова позже.",
        "admin_welcome": "Панель администратора. Выберите действие:",
        "admin_stats": "Статистика",
        "admin_users": "Управление пользователями",
        "admin_logs": "Логи и отчёты",
        "admin_stats_info": "Статистика бота:\n\nВсего пользователей: {total_users}\nАктивных пользователей (7 дней): {active_users}\nПремиум-пользователей: {premium_users}\nСреднее количество лекарств на пользователя: {avg_pills}\nДоход за месяц: {monthly_income}₽",
        "admin_ban_success": "Пользователь {user_id} заблокирован.",
        "admin_unban_success": "Пользователь {user_id} разблокирован.",
        "admin_extend_success": "Подписка пользователя {user_id} продлена на {days} дней.",
        "user_blocked": "Вы были заблокированы администратором. Обратитесь в поддержку для выяснения причин.",
        # "ad_banner": "🔍 Попробуйте новое приложение для отслеживания здоровья! Скачайте сейчас: health-app.com",
        "my_medications": "Мои лекарства",
        "your_medications": "Ваши лекарства:",
        "no_medications": "Вы еще не добавили ни одного лекарства.",
        "custom_pills": "🕒 Своё время:",
        "manage_medications": "Что вы хотите сделать?",
        "delete_medication": "Удалить лекарство",
        "select_medication_to_delete": "Выберите лекарство для удаления:",
        "cancel": "Отмена",
        "deletion_cancelled": "Операция отменена.",
        "medication_not_found": "Лекарство не найдено.",
        "confirm_delete_medication": "Вы уверены, что хотите удалить {name}?",
        "confirm_delete": "Да, удалить",
        "medication_deleted": "Лекарство {name} удалено.",
        "reminder_settings": "Настройки напоминаний",
        "reminders_enabled": "Напоминания включены",
        "reminders_disabled": "Напоминания отключены",
        "enable_reminders": "Включить напоминания",
        "disable_reminders": "Отключить напоминания",
        "reminder_repeat_time": "Повторять напоминание через:",
        "5_minutes": "5 минут",
        "15_minutes": "15 минут",
        "30_minutes": "30 минут",
        "reminder_settings_updated": "Настройки напоминаний обновлены",
        "take_now": "Принять сейчас",
        "snooze": "Отложить",
        "disable_this_reminder": "Отключить это напоминание",
        "reminder_disabled": "Напоминание отключено",
        "snoozed_for": "Напоминание отложено на {minutes} минут",
        "change_language": "Сменить язык",
        "limit_reached": "Вы не можете добавить более 5 лекарств. Перейдите на Premium для снятия ограничений.",
        "premium_status_active": "🌟 Ваш Premium активен до {expiry_date}",
        "premium_status_inactive": "🔒 Premium неактивен",
        "trial_activated": "🎁 Вы активировали 30-дневный пробный период Premium!",
    },
    "en": {
        "welcome": "Welcome to MedReminder! I will help you remember to take your medications on time.",
        "language_selected": "You have selected English language.",
        "select_language": "Select language / Выберите язык:",
        "main_menu": "Main menu:",
        "add_pill": "Add medication",
        "today_pills": "Today's medications",
        "settings": "Settings",
        "subscription": "Subscription",
        "enter_pill_name": "Enter the medication name:",
        "select_schedule": "Select intake schedule:",
        "morning": "Morning",
        "day": "Day",
        "evening": "Evening",
        "custom_time": "Custom time",
        "select_time": "Select intake time:",
        "enter_custom_time": "Enter your custom time in HH:MM format (e.g., 08:30):",
        "invalid_time_format": "Invalid time format. Please use HH:MM format (e.g., 08:30).",
        "pill_added": "Medication {name} added at {time}",
        "no_pills_today": "No medications scheduled for today.",
        "today_checklist": "Your checklist for today ({date}):",
        "morning_pills": "🌅 Morning:",
        "day_pills": "☀️ Day:",
        "evening_pills": "🌙 Evening:",
        "pill_item": "{name} - {time}",
        "mark_as_taken": "✅ Taken",
        "marked_as_taken": "Marked as taken: {name}",
        "reminder": "Reminder: Time to take {name}!",
        "reminder_repeat": "Reminder: You haven't marked {name} as taken yet!",
        "subscription_info": "Subscription information:",
        "free_plan": "You have a free plan. Ads are shown in reminders.",
        "premium_plan": "You have a premium subscription until {date}.",
        "lifetime_plan": "You have a lifetime premium subscription.",
        "subscription_plans": "Subscription plans:",
        "monthly_plan": "Monthly - $1.99",
        "yearly_plan": "Yearly - $9.99",
        "lifetime_plan_purchase": "Lifetime - $24.99",
        "subscription_expiring": "Your subscription expires tomorrow. Would you like to renew?",
        "subscription_expired": "Your subscription has expired. You are now using the free plan with ads.",
        "payment_success": "Payment successful! Your subscription has been activated.",
        "payment_failed": "Payment failed. Please try again later.",
        "admin_welcome": "Admin panel. Choose an action:",
        "admin_stats": "Statistics",
        "admin_users": "User management",
        "admin_logs": "Logs and reports",
        "admin_stats_info": "Bot statistics:\n\nTotal users: {total_users}\nActive users (7 days): {active_users}\nPremium users: {premium_users}\nAverage medications per user: {avg_pills}\nMonthly income: ${monthly_income}",
        "admin_ban_success": "User {user_id} has been banned.",
        "admin_unban_success": "User {user_id} has been unbanned.",
        "admin_extend_success": "User {user_id} subscription extended by {days} days.",
        "user_blocked": "You have been blocked by the administrator. Please contact support for more information.",
        # "ad_banner": "🔍 Try the new health tracking app! Download now: health-app.com",
        "my_medications": "My medications",
        "your_medications": "Your medications:",
        "no_medications": "You haven't added any medications yet.",
        "custom_pills": "🕒 Custom time:",
        "manage_medications": "What would you like to do?",
        "delete_medication": "Delete medication",
        "select_medication_to_delete": "Select medication to delete:",
        "cancel": "Cancel",
        "deletion_cancelled": "Operation cancelled.",
        "medication_not_found": "Medication not found.",
        "confirm_delete_medication": "Are you sure you want to delete {name}?",
        "confirm_delete": "Yes, delete",
        "medication_deleted": "Medication {name} has been deleted.",
        "reminder_settings": "Reminder Settings",
        "reminders_enabled": "Reminders are enabled",
        "reminders_disabled": "Reminders are disabled",
        "enable_reminders": "Enable reminders",
        "disable_reminders": "Disable reminders",
        "reminder_repeat_time": "Repeat reminder after:",
        "5_minutes": "5 minutes",
        "15_minutes": "15 minutes",
        "30_minutes": "30 minutes",
        "reminder_settings_updated": "Reminder settings updated",
        "take_now": "Take now",
        "snooze": "Snooze",
        "disable_this_reminder": "Disable this reminder",
        "reminder_disabled": "Reminder disabled",
        "snoozed_for": "Reminder snoozed for {minutes} minutes",
        "change_language": "Change language",
        "limit_reached": "You can't add more than 5 medications. Upgrade to Premium for unlimited access.",
        "premium_status_active": "🌟 Ваш Premium активен до {expiry_date}",
        "premium_status_inactive": "🔒 Premium неактивен",
        "trial_activated": "🎁 Вы активировали 30-дневный пробный период Premium!",
    }
}

def get_text(key: str, language: str, **kwargs: Any) -> str:
    """Get localized text by key and language with optional formatting"""
    language = language if language in TEXTS else "en"
    text = TEXTS[language].get(key, TEXTS["en"].get(key, f"Missing text for: {key}"))
    if kwargs:
        return text.format(**kwargs)
    return text

```

### END_FILE:utils/localization.py

### BEGIN_FILE:utils/logger.py

**Path:** `utils/logger.py`  
**Language:** Python  
**Description:** Configure logging  
**Last Modified:** 2025-04-02T13:42:26.906388  
**MD5 Hash:** 0f0a91e2f3a755ee5d74bcb0863ab511  

```python
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/bot_{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("med_reminder_bot")

def log_info(message: str) -> None:
    logger.info(message)

def log_error(message: str, exc_info=None) -> None:
    logger.error(message, exc_info=exc_info)

def log_warning(message: str) -> None:
    logger.warning(message)

def log_user_action(user_id: int, action: str, details: str = None) -> None:
    message = f"User {user_id}: {action}"
    if details:
        message += f" - {details}"
    log_info(message)

def log_payment(user_id: int, amount: float, plan: str, status: str) -> None:
    log_info(f"Payment: User {user_id} - {plan} plan ({amount}) - Status: {status}")

def log_admin_action(admin_id: int, action: str, target_user_id: int = None) -> None:
    message = f"ADMIN {admin_id}: {action}"
    if target_user_id:
        message += f" - Target user: {target_user_id}"
    log_info(message)

```

### END_FILE:utils/logger.py

### BEGIN_FILE:utils/states.py

**Path:** `utils/states.py`  
**Language:** Python  
**Description:** from aiogram.fsm.state import State, StatesGroup  
**Last Modified:** 2025-04-02T13:42:04.192564  
**MD5 Hash:** c4c9afafd7308f1c9212b494a9d9dad9  

```python
from aiogram.fsm.state import State, StatesGroup

class AddPillStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_schedule = State()
    waiting_for_time = State()
    waiting_for_custom_time = State()

class SettingsStates(StatesGroup):
    waiting_for_language = State()

class AdminStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_days = State()

```

### END_FILE:utils/states.py

