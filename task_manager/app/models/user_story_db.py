from sqlalchemy import Column, Integer, String, Text, Enum, Float, DateTime, func
from .enums import PriorityEnum
from app.database.azure_connection import Base

class UserStory(Base):
    __tablename__ = "user_story"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    goal = Column(String(255), nullable=False)
    reason = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Enum(PriorityEnum), nullable=False)
    story_points = Column(Integer, nullable=False)
    effort_hours = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 