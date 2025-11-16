from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pull_request_model import PullRequest
from app.models.pull_request_reviewer_model import PullRequestReviewer
from app.models.user_model import User


class StatsRepository:
    @staticmethod
    async def get_stats(session: AsyncSession):
        total_pr = await session.scalar(select(func.count(PullRequest.id)))
        open_pr = await session.scalar(
            select(func.count()).where(PullRequest.status == "OPEN")
        )
        merged_pr = await session.scalar(
            select(func.count()).where(PullRequest.status == "MERGED")
        )
        total_assignments = await session.scalar(
            select(func.count(PullRequestReviewer.id))
        )
        rows = await session.execute(
            select(User.user_id, func.count(PullRequestReviewer.id))
            .join(PullRequestReviewer, PullRequestReviewer.reviewer_id == User.id)
            .group_by(User.user_id)
        )
        assignments_by_user = {row[0]: row[1] for row in rows}

        rows = await session.execute(
            select(User.user_id, func.count(PullRequest.id))
            .join(User, PullRequest.author_id == User.id)
            .group_by(User.user_id)
        )
        pr_by_author = {row[0]: row[1] for row in rows}

        return {
            "total_pr": total_pr,
            "open_pr": open_pr,
            "merged_pr": merged_pr,
            "total_assignments": total_assignments,
            "assignments_by_user": assignments_by_user,
            "pr_by_author": pr_by_author,
        }
