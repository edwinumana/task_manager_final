from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.enums import PriorityEnum
from datetime import datetime

class UserStorySchema(BaseModel):
    id: Optional[int]
    project: str
    role: str
    goal: str
    reason: str
    description: str
    priority: PriorityEnum
    story_points: int
    effort_hours: float
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class UserStorySchemas(BaseModel):
    user_stories: List[UserStorySchema] 