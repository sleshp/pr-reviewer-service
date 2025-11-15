from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base


class PullRequestReviewer(Base):
    __tablename__ = "pull_request_reviewers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pull_request_id = Column(
        Integer, ForeignKey("pull_requests.id", ondelete="CASCADE"), nullable=False
    )
    reviewer_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    position = Column(SmallInteger, nullable=False)

    pull_request = relationship("PullRequest", back_populates="reviewers")
    reviewer = relationship("User", back_populates="reviews")

    __table_args__ = (
        UniqueConstraint("pull_request_id", "reviewer_id", name="uq_pr_reviewer_user"),
        UniqueConstraint("pull_request_id", "position", name="uq_pr_reviewer_position"),
    )
