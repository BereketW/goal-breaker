from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SubTaskBase(BaseModel):
    description: str
    complexity_score: int

class SubTaskCreate(SubTaskBase):
    pass

class SubTask(SubTaskBase):
    id: int
    goal_id: int

    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    description: str

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: int
    created_at: datetime
    subtasks: List[SubTask] = []

    class Config:
        from_attributes = True
