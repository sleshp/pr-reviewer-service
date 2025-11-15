from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.team_repository import TeamRepository
from app.repositories.user_repository import UserRepository
from app.schemas.team_schema import Team, TeamMember


class TeamService:
    @staticmethod
    async def create_team(
        session: AsyncSession,
        team_name: str,
        members: list[TeamMember],
    ) -> Team:
        existing = await TeamRepository.get_by_name(session, team_name)
        if existing:
            raise ValueError("TEAM_EXISTS")

        team = await TeamRepository.create(session, team_name)

        for member in members:
            existing_user = await UserRepository.get_by_user_id(session, member.user_id)
            if existing_user:
                await UserRepository.update_for_team(
                    session=session,
                    user=existing_user,
                    username=member.username,
                    is_active=member.is_active,
                    team_id=team.id,
                )
            else:
                await UserRepository.create(
                    session=session,
                    user_id=member.user_id,
                    username=member.username,
                    is_active=member.is_active,
                    team_id=team.id,
                )
        await session.commit()

        members_db = await TeamRepository.list_members(session, team.id)

        return Team(
            team_name=team.team_name,
            members=[
                TeamMember(
                    user_id=m.user_id,
                    username=m.username,
                    is_active=m.is_active,
                )
                for m in members_db
            ],
        )

    @staticmethod
    async def get_team(
        session: AsyncSession,
        team_name: str,
    ) -> Team:
        team = await TeamRepository.get_by_name(session, team_name)
        if not team:
            raise ValueError("NOT_FOUND")

        members = await TeamRepository.list_members(session, team.id)

        return Team(
            team_name=team.team_name,
            members=[
                TeamMember(
                    user_id=m.user_id,
                    username=m.username,
                    is_active=m.is_active,
                )
                for m in members
            ],
        )
