import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_session
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_session_factory():
    engine = create_async_engine(DATABASE_URL, future=True)
    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_session_maker
    await engine.dispose()


@pytest.fixture(scope="function")
async def override_get_session(async_session_factory):
    async def _get_session_override():
        async with async_session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = _get_session_override
    yield
    app.dependency_overrides.clear()
