import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = os.getenv(
    "DATABASE_URL",
)

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured."
    )

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

DATABASE_URL = DATABASE_URL.replace("sslmode=require", "ssl=require")
DATABASE_URL = DATABASE_URL.replace("&channel_binding=disable", "")
DATABASE_URL = DATABASE_URL.replace("?channel_binding=disable", "")

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as session:
        yield session