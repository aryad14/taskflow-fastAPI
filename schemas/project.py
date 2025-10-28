from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .task import TaskRead

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    tasks: List[TaskRead] = []

    class Config:
        orm_mode = True
