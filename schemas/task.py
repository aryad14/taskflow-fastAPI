from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    user_id: int

class TaskCreate(TaskBase):
    project_id: int
    assigned_to: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Design homepage",
                    "description": "Create hero section and navigation",
                    "project_id": 1,
                    "assigned_to": 2
                }
            ]
        }
    )

class TaskRead(TaskBase):
    id: int
    user_id: int
    project_id: int
    assigned_to: Optional[int]
    created_at: datetime

    # Pydantic v2: enable ORM attribute parsing + example
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 10,
                    "title": "Design homepage",
                    "description": "Create hero section and navigation",
                    "is_completed": False,
                    "user_id": 1,
                    "project_id": 1,
                    "assigned_to": 2,
                    "created_at": "2025-01-15T10:00:00Z"
                }
            ]
        }
    )

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    assigned_to: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Design homepage v2",
                    "description": "Add animation to hero section",
                    "is_completed": True,
                    "assigned_to": 3
                }
            ]
        }
    )