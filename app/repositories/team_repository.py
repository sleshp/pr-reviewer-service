from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team_model import Team
from app.models.user_model import User


class TeamRepository:

    @staticmethod
    async def create(session: AsyncSession, team_name: str) -> Team:
        team = Team(team_name=team_name)
        session.add(team)
        await session.flush()
        return team

    @staticmethod
    async def get_by_name(session: AsyncSession, team_name: str) -> Team | None:
        stmt = select(Team).where(Team.team_name == team_name)
        result = await session.scalars(stmt)
        return result.first()

    @staticmethod
    async def list_members(session: AsyncSession, team_id: int) -> list[User]:
        result = await session.scalars(select(User).where(User.team_id == team_id))
        return list(result)
