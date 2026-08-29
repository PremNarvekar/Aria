import asyncio

from sqlalchemy import text

from .database import SessionLocal


async def test_connection() -> None:

    async with SessionLocal() as session:

        result = await session.execute(
            text("SELECT 1")
        )

        print(
            "Database connection:",
            result.scalar(),
        )


if __name__ == "__main__":
    asyncio.run(test_connection())