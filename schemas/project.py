from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from .task import TaskRead

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    # Pydantic v2: example for Swagger
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Website Redesign",
                    "description": "Redesign the company website with a new brand look."
                }
            ]
        }
    )

class ProjectRead(ProjectBase):
    id: int
    tasks: List[TaskRead] = Field(default_factory=list)

    # Pydantic v2: enable ORM attribute parsing + example
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "title": "Website Redesign",
                    "description": "Redesign the company website with a new brand look.",
                    "created_at": "2025-01-15T10:00:00Z",
                    "tasks": []
                }
            ]
        }
    )

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Website Revamp",
                    "description": "Update branding and improve accessibility."
                }
            ]
        }
    )
