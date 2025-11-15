from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String, unique=True, nullable=False)

    members = relationship("User", back_populates="team")
