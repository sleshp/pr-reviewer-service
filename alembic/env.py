from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config

from alembic import context
from app.db import Base
from app.models.pull_request_model import PullRequest
from app.models.pull_request_reviewer_model import PullRequestReviewer
from app.models.team_model import Team
from app.models.user_model import User

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
