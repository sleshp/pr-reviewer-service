from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.pull_request_schema import (
    PullRequest,
    PullRequestResponse,
    ReassignReviewerResponse,
)
from app.schemas.requests_schema import (
    PullRequestCreateRequest,
    PullRequestReassignRequest,
)
from app.services.pull_request_service import PullRequestService

router = APIRouter()


@router.post("/create", response_model=PullRequestResponse, status_code=201)
async def create_pr(
    data: PullRequestCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    pr = await PullRequestService.create_pr(
        session=session,
        pull_request_id=data.pull_request_id,
        pull_request_name=data.pull_request_name,
        author_user_id=data.author_id,
    )
    return PullRequestResponse(pr=pr)


@router.post("/merge", response_model=PullRequestResponse)
async def merge_pr(
    pull_request_id: str,
    session: AsyncSession = Depends(get_session),
):
    pr = await PullRequestService.merge_pr(
        session=session,
        pull_request_id=pull_request_id,
    )
    return PullRequestResponse(pr=pr)


@router.post("/reassignReviewer", response_model=ReassignReviewerResponse)
async def reassign_reviewer(
    data: PullRequestReassignRequest,
    session: AsyncSession = Depends(get_session),
):
    pr, replaced_by = await PullRequestService.reassign_reviewer(
        session=session,
        pull_request_id=data.pull_request_id,
        old_reviewer_user_id=data.old_reviewer_id,
    )
    return ReassignReviewerResponse(pr=pr, replaced_by=replaced_by)
