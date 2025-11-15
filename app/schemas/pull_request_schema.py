from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class PRStatus(str, Enum):
    OPEN = "OPEN"
    MERGED = "MERGED"


class PullRequestBase(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: PRStatus


class PullRequest(PullRequestBase):
    assigned_reviewers: List[str]
    createdAt: Optional[datetime]
    mergedAt: Optional[datetime]


class PullRequestShort(PullRequestBase):
    pass


class ReassignReviewerResponse(BaseModel):
    pr: PullRequest
    replaced_by: str


class PullRequestResponse(BaseModel):
    pr: PullRequest
