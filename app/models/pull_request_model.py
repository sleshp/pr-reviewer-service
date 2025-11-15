import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class PRStatus(str, enum.Enum):
    OPEN = "OPEN"
    MERGED = "MERGED"


class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pull_request_id = Column(String, unique=True, nullable=False)
    pull_request_name = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(PRStatus), nullable=False, default=PRStatus.OPEN)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    merged_at = Column(DateTime(timezone=True), nullable=True)

    author = relationship("User", back_populates="authored_prs")
    reviewers = relationship(
        "PullRequestReviewer",
        back_populates="pull_request",
        cascade="all, delete-orphan",
        order_by="PullRequestReviewer.position",
    )
