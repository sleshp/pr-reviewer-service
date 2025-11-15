import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://pr_user:pr_pass@db:5432/pr_service",
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)


AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


Base = declarative_base()


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
