from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

class TaskCreate(TaskBase):
    project_id: int
    assigned_to: Optional[int] = None

class TaskRead(TaskBase):
    id: int
    project_id: int
    assigned_to: Optional[int]
    created_at: datetime

    # Pydantic v2: enable ORM attribute parsing
    model_config = ConfigDict(from_attributes=True)
