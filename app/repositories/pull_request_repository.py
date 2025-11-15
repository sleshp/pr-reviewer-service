from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pull_request_model import PRStatus, PullRequest


class PullRequestRepository:
    @staticmethod
    async def create(
        session: AsyncSession,
        pull_request_id: str,
        pull_request_name: str,
        author_db_id: int,
    ) -> PullRequest:
        pr = PullRequest(
            pull_request_id=pull_request_id,
            pull_request_name=pull_request_name,
            author_id=author_db_id,
        )
        session.add(pr)
        await session.flush()
        return pr

    @staticmethod
    async def get_by_pr_id(
        session: AsyncSession,
        pr_id: str,
    ) -> PullRequest | None:
        return await session.scalar(
            select(PullRequest).where(PullRequest.pull_request_id == pr_id)
        )

    @staticmethod
    async def list_by_reviewer_db_id(
        session: AsyncSession,
        reviewer_db_id: int,
    ) -> list[PullRequest]:
        from app.models.pull_request_reviewer_model import PullRequestReviewer

        prs = await session.scalars(
            select(PullRequest)
            .join(PullRequestReviewer)
            .where(PullRequestReviewer.reviewer_id == reviewer_db_id)
        )
        return list(prs)

    @staticmethod
    async def set_merged(
        session: AsyncSession,
        pr: PullRequest,
    ) -> PullRequest:
        pr.status = PRStatus.MERGED
        pr.merged_at = datetime.now(timezone.utc)
        await session.flush()
        return pr
