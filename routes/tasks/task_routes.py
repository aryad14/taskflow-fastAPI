from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from schemas.task import TaskCreate, TaskRead, TaskUpdate
from schemas.response import ApiResponse
from utils.responses import response
from utils.exceptions import AppException
from core.dependencies import get_db_session, get_current_user
from services.task_service import (
    create_task as svc_create_task,
    get_tasks_for_project,
    update_task as svc_update_task,
    delete_task as svc_delete_task,
    get_task_by_id as svc_get_task_by_id,
)

router = APIRouter(prefix="/tasks", tags=["Task Management"])

@router.post("/", response_model=ApiResponse[TaskRead])
async def create_task(
    request: Request,
    task: TaskCreate,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user),
):
    """
    Create a task under a project owned by the current user.
    """
    try:
        created = svc_create_task(db, current_user.id, task)
        if not created:
            raise AppException("Project not found or not accessible", status_code=404)
        return response(
            True,
            "Task created successfully",
            data=TaskRead.model_validate(created).model_dump(),
        )
    except AppException:
        raise
    except Exception as e:
        raise AppException(str(e))

@router.get("/project/{project_id}", response_model=ApiResponse[List[TaskRead]])
async def list_tasks_for_project(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user),
):
    """
    List tasks for a specific project owned by the current user.
    """
    try:
        tasks = get_tasks_for_project(db, current_user.id, project_id)
        # If empty, either no tasks or project not accessible; return empty list
        data = [TaskRead.model_validate(t).model_dump() for t in tasks]
        return response(True, "Tasks fetched successfully", data=data)
    except Exception as e:
        raise AppException(str(e))

@router.get("/{task_id}", response_model=ApiResponse[TaskRead])
async def get_task(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user),
):
    try:
        task = svc_get_task_by_id(db, current_user.id, task_id)
        if not task:
            raise AppException("Task not found", status_code=404)
        return response(True, "Task fetched successfully", data=TaskRead.model_validate(task).model_dump())
    except AppException:
        raise
    except Exception as e:
        raise AppException(str(e))

@router.put("/{task_id}", response_model=ApiResponse[TaskRead])
async def update_task(
    request: Request,
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user),
):
    try:
        updated = svc_update_task(db, current_user.id, task_id, task)
        if not updated:
            raise AppException("Task not found", status_code=404)
        return response(True, "Task updated successfully", data=TaskRead.model_validate(updated).model_dump())
    except AppException:
        raise
    except Exception as e:
        raise AppException(str(e))

@router.delete("/{task_id}", response_model=ApiResponse[None])
async def delete_task(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_user),
):
    try:
        deleted = svc_delete_task(db, current_user.id, task_id)
        if not deleted:
            raise AppException("Task not found", status_code=404)
        return response(True, "Task deleted successfully", data=None)
    except AppException:
        raise
    except Exception as e:
        raise AppException(str(e))