from pydantic import BaseModel, Field, ConfigDict
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
    created_at: datetime
    # Avoid mutable default list
    tasks: List[TaskRead] = Field(default_factory=list)

    # Pydantic v2: enable ORM attribute parsing
    model_config = ConfigDict(from_attributes=True)
    
class ProjectUpdate(ProjectBase):
    pass
