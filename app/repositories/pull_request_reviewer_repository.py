from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pull_request_reviewer_model import PullRequestReviewer


class PullRequestReviewerRepository:

    @staticmethod
    async def add_reviewer(
        session: AsyncSession, pr_db_id: int, reviewer_db_id: int, position: int
    ) -> PullRequestReviewer:
        link = PullRequestReviewer(
            pull_request_id=pr_db_id, reviewer_id=reviewer_db_id, position=position
        )
        session.add(link)
        await session.flush()
        return link

    @staticmethod
    async def list_by_pr_db_id(
        session: AsyncSession, pr_db_id: int
    ) -> list[PullRequestReviewer]:
        links = await session.scalars(
            select(PullRequestReviewer)
            .where(PullRequestReviewer.pull_request_id == pr_db_id)
            .order_by(PullRequestReviewer.position)
        )
        return list(links)

    @staticmethod
    async def get_by_pr_and_reviewer(
        session: AsyncSession, pr_db_id: int, reviewer_db_id: int
    ) -> PullRequestReviewer | None:
        return await session.scalar(
            select(PullRequestReviewer).where(
                PullRequestReviewer.pull_request_id == pr_db_id,
                PullRequestReviewer.reviewer_id == reviewer_db_id,
            )
        )

    @staticmethod
    async def update_reviewer(
        session: AsyncSession, link: PullRequestReviewer, new_reviewer_db_id: int
    ) -> PullRequestReviewer:
        link.reviewer_id = new_reviewer_db_id
        await session.flush()
        return link
