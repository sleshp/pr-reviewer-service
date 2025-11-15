from typing import List

from pydantic import BaseModel

from .team import TeamMember


class TeamCreateRequest(BaseModel):
    team_name: str
    members: List[TeamMember]


class UserSetActiveRequest(BaseModel):
    user_id: str
    is_active: bool


class PullRequestCreateRequest(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str


class PullRequestReassignRequest(BaseModel):
    pull_request_id: str
    old_reviewer_id: str
