from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.task import TaskCreate, TaskRead, TaskUpdate
from models.task import Task

from utils.responses import response
from utils.exceptions import AppException

from core.dependencies import get_db_session, get_current_user
from services.task_service import get_tasks, create_task, delete_task, update_task

router = APIRouter(prefix="/tasks", tags=["Task Management"])

@router.get("/", response_model=dict)
def read_tasks(
    db: Session = Depends(get_db_session),
    current_user: Task = Depends(get_current_user)
):
    tasks = get_tasks(db, current_user.id)
    tasks_data = [TaskRead.model_validate(task).model_dump() for task in tasks]
    return response(True, "Tasks fetched successfully", data=tasks_data)

@router.post("/", response_model=dict)
def create_new_task(
    task_create: TaskCreate,
    db: Session = Depends(get_db_session),
    current_user: Task = Depends(get_current_user)
):
    task = create_task(db, task_create.title, current_user.id)
    return response(True, "Task created successfully", data=TaskRead.model_validate(task).model_dump())

@router.delete("/{task_id}", response_model=dict)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db_session),
    current_user: Task = Depends(get_current_user)
):
    task = delete_task(db, task_id, current_user.id)
    if not task:
        raise AppException("Task not found or unauthorized", status_code=404)
    return response(True, "Task deleted successfully")

@router.put("/{task_id}", response_model=dict)
def update_existing_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db_session),
    current_user: Task = Depends(get_current_user)
):
    task = update_task(db, task_id, task_update.title, current_user.id)
    if not task:
        raise AppException("Task not found or unauthorized", status_code=404)
    return response(True, "Task updated successfully", data=TaskRead.model_validate(task).model_dump())

