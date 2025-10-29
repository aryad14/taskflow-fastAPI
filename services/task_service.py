from typing import List, Optional
from sqlalchemy.orm import Session
from models.task import Task
from models.project import Project
from schemas.task import TaskCreate, TaskUpdate

def get_tasks_for_project(db: Session, owner_id: int, project_id: int) -> List[Task]:
    # Verify project ownership
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == owner_id).first()
    if not project:
        return []
    return db.query(Task).filter(Task.project_id == project_id, Task.user_id == owner_id).all()

def create_task(db: Session, owner_id: int, task_in: TaskCreate) -> Optional[Task]:
    # Only allow creating tasks in projects owned by the current user
    project = db.query(Project).filter(Project.id == task_in.project_id, Project.owner_id == owner_id).first()
    if not project:
        return None

    data = task_in.model_dump(exclude_unset=True)
    new_task = Task(
        title=data.get("title"),
        description=data.get("description"),
        is_completed=data.get("is_completed", False),
        user_id=owner_id,
        project_id=data["project_id"],
        assigned_to=data.get("assigned_to"),
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_task_by_id(db: Session, owner_id: int, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id, Task.user_id == owner_id).first()

def update_task(db: Session, owner_id: int, task_id: int, task_in: TaskUpdate) -> Optional[Task]:
    task = get_task_by_id(db, owner_id, task_id)
    if not task:
        return None
    data = task_in.model_dump(exclude_unset=True)
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "is_completed" in data:
        task.is_completed = data["is_completed"]
    if "assigned_to" in data:
        task.assigned_to = data["assigned_to"]
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, owner_id: int, task_id: int) -> Optional[Task]:
    task = get_task_by_id(db, owner_id, task_id)
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task