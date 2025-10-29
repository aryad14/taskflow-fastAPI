from typing import List
from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from schemas.response import ApiResponse
from models.project import Project

from utils.responses import response
from utils.exceptions import AppException

from core.dependencies import get_db_session, get_current_user
from services.project_service import (
    get_projects,
    create_project as svc_create_project,
    get_project_by_id,
    update_project as svc_update_project,
    delete_project as svc_delete_project,
)

router = APIRouter(prefix="/projects", tags=["Project Management"])

@router.get("/", response_model=ApiResponse[List[ProjectRead]])
async def list_projects(
    request: Request,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user)
):
    """
    List projects for the current user.
    """
    try:
        projects = get_projects(db, current_user.id)
        projects_data = [ProjectRead.model_validate(p).model_dump() for p in projects]
        return response(data=projects_data, success=True, message="Projects fetched successfully")
    except Exception as e:
        raise AppException(str(e))

@router.post("/", response_model=ApiResponse[ProjectRead])
async def create_project(
    request: Request,
    project: ProjectCreate,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user)
):
    """
    Create a new project.
    """
    try:
        new_project = svc_create_project(db, project, current_user.id)
        return response(
            success=True,
            message="Project created successfully",
            data=ProjectRead.model_validate(new_project).model_dump(),
        )
    except Exception as e:
        raise AppException(str(e))

@router.put("/{project_id}", response_model=ApiResponse[ProjectRead])
async def update_project(
    request: Request,
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user)
):
    """
    Update an existing project.
    """
    try:
        updated = svc_update_project(db, project_id, current_user.id, project)
        if not updated:
            raise AppException("Project not found", status_code=404)
        return response(
            data=ProjectRead.model_validate(updated).model_dump(),
            success=True,
            message="Project updated successfully",
        )
    except AppException:
        raise
    except Exception as e:
        raise AppException(str(e))

@router.delete("/{project_id}", response_model=ApiResponse[None])
async def delete_project(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user)
):
    """
    Delete a project by id.
    """
    try:
        deleted = svc_delete_project(db, project_id, current_user.id)
        if not deleted:
            raise AppException("Project not found", status_code=404)
        return response(message="Project deleted successfully", success=True, data=None)
    except AppException:
        raise
    except Exception as e:
        raise AppException(str(e))