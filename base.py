from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Base


DATABASE_URL = "sqlite+aiosqlite:///./docs/action.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def database_implementation() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
