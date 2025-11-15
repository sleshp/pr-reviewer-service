import random
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pull_request_model import PRStatus
from app.models.team_model import Team
from app.models.user_model import User
from app.repositories.pull_request_repository import PullRequestRepository
from app.repositories.pull_request_reviewer_repository import (
    PullRequestReviewerRepository,
)
from app.repositories.team_repository import TeamRepository
from app.repositories.user_repository import UserRepository
from app.schemas.pull_request_schema import PullRequest


class PullRequestService:
    @staticmethod
    async def create_pr(
        session: AsyncSession,
        pull_request_id: str,
        pull_request_name: str,
        author_user_id: str,
    ) -> PullRequest:
        existing = await PullRequestRepository.get_by_pr_id(session, pull_request_id)
        if existing:
            raise ValueError("PR_EXISTS")

        author = await UserRepository.get_by_user_id(session, author_user_id)
        if not author:
            raise ValueError("NOT_FOUND")

        team = await session.scalar(select(Team).where(Team.id == author.team_id))

        members = await TeamRepository.list_members(session, team.id)
        candidates = [m for m in members if m.is_active and m.id != author.id]

        random.shuffle(candidates)
        reviewers = candidates[:2]

        pr = await PullRequestRepository.create(
            session=session,
            pull_request_id=pull_request_id,
            pull_request_name=pull_request_name,
            author_db_id=author.id,
        )

        for index, user in enumerate(reviewers, start=1):
            await PullRequestReviewerRepository.add_reviewer(
                session=session,
                pr_db_id=pr.id,
                reviewer_db_id=user.id,
                position=index,
            )

        await session.commit()

        return PullRequest(
            pull_request_id=pr.pull_request_id,
            pull_request_name=pr.pull_request_name,
            author_id=author.user_id,
            status=pr.status,
            assigned_reviewers=[u.user_id for u in reviewers],
            createdAt=pr.created_at,
            mergedAt=pr.merged_at,
        )

    @staticmethod
    async def merge_pr(session: AsyncSession, pull_request_id: str) -> PullRequest:
        pr = await PullRequestRepository.get_by_pr_id(session, pull_request_id)
        if not pr:
            raise ValueError("NOT_FOUND")

        author = await session.scalar(select(User).where(User.id == pr.author_id))

        reviewer_links = await PullRequestReviewerRepository.list_by_pr_db_id(
            session, pr.id
        )
        reviewer_user_ids = []
        for link in reviewer_links:
            u = await session.scalar(select(User).where(User.id == link.reviewer_id))
            reviewer_user_ids.append(u.user_id)

        if pr.status == PRStatus.MERGED:
            return PullRequest(
                pull_request_id=pr.pull_request_id,
                pull_request_name=pr.pull_request_name,
                author_id=author.user_id,
                status=pr.status,
                assigned_reviewers=reviewer_user_ids,
                createdAt=pr.created_at,
                mergedAt=pr.merged_at,
            )

        pr.status = PRStatus.MERGED
        pr.merged_at = datetime.now(timezone.utc)

        await session.commit()

        return PullRequest(
            pull_request_id=pr.pull_request_id,
            pull_request_name=pr.pull_request_name,
            author_id=author.user_id,
            status=pr.status,
            assigned_reviewers=reviewer_user_ids,
            createdAt=pr.created_at,
            mergedAt=pr.merged_at,
        )

    @staticmethod
    async def reassign_reviewer(
        session: AsyncSession,
        pull_request_id: str,
        old_reviewer_user_id: str,
    ) -> PullRequest:
        pr = await PullRequestRepository.get_by_pr_id(session, pull_request_id)
        if not pr:
            raise ValueError("NOT_FOUND")

        if pr.status == PRStatus.MERGED:
            raise ValueError("PR_MERGED")

        old_reviewer = await UserRepository.get_by_user_id(
            session, old_reviewer_user_id
        )
        if not old_reviewer:
            raise ValueError("NOT_FOUND")

        link = await PullRequestReviewerRepository.get_by_pr_and_reviewer(
            session=session,
            pr_db_id=pr.id,
            reviewer_db_id=old_reviewer.id,
        )
        if not link:
            raise ValueError("NOT_ASSIGNED")

        team_members = await TeamRepository.list_members(
            session, team_id=old_reviewer.team_id
        )

        reviewers_links = await PullRequestReviewerRepository.list_by_pr_db_id(
            session, pr.id
        )

        current_reviewer_ids = {r.reviewer_id for r in reviewers_links}
        current_reviewer_ids.add(pr.author_id)

        candidates = [
            m for m in team_members if m.is_active and m.id not in current_reviewer_ids
        ]

        if not candidates:
            raise ValueError("NO_CANDIDATE")

        random.shuffle(candidates)
        new_reviewer = candidates[0]

        await PullRequestReviewerRepository.update_reviewer(
            session=session,
            link=link,
            new_reviewer_db_id=new_reviewer.id,
        )

        updated_links = await PullRequestReviewerRepository.list_by_pr_db_id(
            session, pr.id
        )
        await session.commit()

        return (
            PullRequest(
                pull_request_id=pr.pull_request_id,
                pull_request_name=pr.pull_request_name,
                author_id=(
                    await session.scalar(select(User).where(User.id == pr.author_id))
                ).user_id,
                status=pr.status,
                assigned_reviewers=[
                    (
                        await session.scalar(
                            select(User).where(User.id == r.reviewer_id)
                        )
                    ).user_id
                    for r in updated_links
                ],
                createdAt=pr.created_at,
                mergedAt=pr.merged_at,
            ),
            new_reviewer.user_id,
        )
