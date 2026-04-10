from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = None
async_session_maker = None
_initialized = False


class Base(DeclarativeBase):
    pass


def configure_engine(url: str | URL) -> None:
    global engine, async_session_maker, _initialized
    if _initialized:
        raise RuntimeError("Database engine already configured")
    engine = create_async_engine(url, echo=False)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    _initialized = True


async def init_db() -> None:
    if engine is None:
        raise RuntimeError("Database engine is not configured")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if async_session_maker is None:
        raise RuntimeError("Database session maker is not configured")
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
