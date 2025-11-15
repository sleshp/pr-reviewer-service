from typing import List

from pydantic import BaseModel

from app.schemas.pull_request_schema import PullRequestShort


class User(BaseModel):
    user_id: str
    username: str
    team_name: str
    is_active: bool


class UserReviewsResponse(BaseModel):
    user_id: str
    pull_requests: List[PullRequestShort]


class UserResponse(BaseModel):
    user: User
