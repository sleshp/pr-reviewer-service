from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team_model import Team
from app.models.user_model import User as UserModel
from app.repositories.pull_request_repository import PullRequestRepository
from app.repositories.user_repository import UserRepository
from app.schemas.pull_request_schema import PullRequestShort
from app.schemas.user_schema import User


class UserService:
    @staticmethod
    async def set_is_active(
        session: AsyncSession,
        user_id: str,
        value: bool,
    ) -> User:
        user = await UserRepository.get_by_user_id(session, user_id)
        if not user:
            raise ValueError("NOT_FOUND")

        await UserRepository.update_is_active(session, user, value)

        team = await session.scalar(select(Team).where(Team.id == user.team_id))

        return User(
            user_id=user.user_id,
            username=user.username,
            team_name=team.team_name if team else "",
            is_active=user.is_active,
        )

    @staticmethod
    async def get_reviews(
        session: AsyncSession,
        user_id: str,
    ) -> list[PullRequestShort]:
        reviewer = await UserRepository.get_by_user_id(session, user_id)
        if not reviewer:
            raise ValueError("NOT_FOUND")

        prs = await PullRequestRepository.list_by_reviewer_db_id(
            session=session,
            reviewer_db_id=reviewer.id,
        )

        result: list[PullRequestShort] = []

        for pr in prs:
            author = await session.scalar(
                select(UserModel).where(UserModel.id == pr.author_id)
            )

            result.append(
                PullRequestShort(
                    pull_request_id=pr.pull_request_id,
                    pull_request_name=pr.pull_request_name,
                    author_id=author.user_id,
                    status=pr.status,
                )
            )

        return result
