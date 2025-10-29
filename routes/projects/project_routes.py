from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from models.project import Project

from utils.responses import response
from utils.exceptions import AppException

from core.dependencies import get_db_session, get_current_user
from services.task_service import get_tasks, create_task, delete_task, update_task

router = APIRouter(prefix="/projects", tags=["Project Management"])

@router.get("/", response_model=dict)
async def list_projects(
    request: Request,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user)
):
    try:
        projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
        projects_data = [ProjectRead.model_validate(p).model_dump() for p in projects]
        return response(data=projects_data, success=True, message="Projects fetched successfully")
    except Exception as e:
        raise AppException(str(e))
    
@router.post("/", response_model=dict)
async def create_project(
    request: Request,
    project: ProjectCreate,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user)
):
    try:
        new_project = Project(**project.dict(), owner_id=current_user.id)
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return response(success=True, message="Project created successfully", data=ProjectRead.model_validate(new_project).model_dump())
    except Exception as e:
        raise AppException(str(e))
    
@router.put("/{project_id}", response_model=dict)
async def update_project(
    request: Request,
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user)
):
    try:
        existing_project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
        if not existing_project:
            raise AppException("Project not found", status_code=404)
        
        for key, value in project.dict(exclude_unset=True).items():
            setattr(existing_project, key, value)
        
        db.commit()
        db.refresh(existing_project)
        return response(data=ProjectRead.model_validate(existing_project).model_dump(), success=True, message="Project updated successfully")
    except Exception as e:
        raise AppException(str(e))
    
@router.delete("/{project_id}")
async def delete_project(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user)
):
    try:
        existing_project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
        if not existing_project:
            raise AppException("Project not found", status_code=404)
        
        db.delete(existing_project)
        db.commit()
        return response(message="Project deleted successfully", success=True, data=None)
    except Exception as e:
        raise AppException(str(e))