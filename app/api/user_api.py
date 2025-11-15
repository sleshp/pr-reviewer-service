from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.pull_request import PullRequestShort
from app.schemas.requests import UserSetActiveRequest
from app.schemas.user import User, UserResponse, UserReviewsResponse
from app.services.user_service import UserService

router = APIRouter()


@router.post("/setIsActive", response_model=UserResponse)
async def set_is_active(
    data: UserSetActiveRequest,
    session: AsyncSession = Depends(get_session),
):
    user = await UserService.set_is_active(
        session=session,
        user_id=data.user_id,
        value=data.is_active,
    )
    return UserResponse(user=user)


@router.get("/getReview", response_model=UserReviewsResponse)
async def get_review(user_id: str, session: AsyncSession = Depends(get_session)):
    prs = await UserService.get_reviews(session, user_id)
    return UserReviewsResponse(user_id=user_id, pull_requests=prs)
