from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User


class UserRepository:
    @staticmethod
    async def create(
        session: AsyncSession,
        user_id: str,
        username: str,
        is_active: bool,
        team_id: int,
    ) -> User:
        user = User(
            user_id=user_id,
            username=username,
            is_active=is_active,
            team_id=team_id,
        )
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    async def get_by_user_id(session: AsyncSession, user_id: str) -> User | None:
        return await session.scalar(select(User).where(User.user_id == user_id))

    @staticmethod
    async def update_is_active(
        session: AsyncSession,
        user: User,
        value: bool,
    ) -> User:
        user.is_active = value
        await session.flush()
        return user

    @staticmethod
    async def update_for_team(
        session: AsyncSession,
        user: User,
        username: str,
        is_active: bool,
        team_id: int,
    ) -> User:
        user.username = username
        user.is_active = is_active
        user.team_id = team_id
        await session.flush()
        return user

    @staticmethod
    async def list_by_team(session: AsyncSession, team_id: int) -> list[User]:
        users = await session.scalars(select(User).where(User.team_id == team_id))
        return list(users)
