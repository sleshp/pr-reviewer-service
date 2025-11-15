from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    team = relationship("Team", back_populates="members")

    authored_prs = relationship("PullRequest", back_populates="author")
    reviews = relationship("PullRequestReviewer", back_populates="reviewer")
