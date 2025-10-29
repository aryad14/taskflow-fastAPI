from typing import List, Optional
from sqlalchemy.orm import Session
from models.project import Project
from schemas.project import ProjectCreate, ProjectUpdate

def get_projects(db: Session, user_id: int) -> List[Project]:
    return db.query(Project).filter(Project.owner_id == user_id).all()

def create_project(db: Session, project_in: ProjectCreate, owner_id: int) -> Project:
    # Only persist valid model columns
    data = project_in.model_dump(exclude_unset=True)
    new_project = Project(
        title=data.get("title"),
        description=data.get("description"),
        owner_id=owner_id,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_project_by_id(db: Session, project_id: int, owner_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id, Project.owner_id == owner_id).first()

def delete_project(db: Session, project_id: int, owner_id: int) -> Optional[Project]:
    project = get_project_by_id(db, project_id, owner_id)
    if project:
        db.delete(project)
        db.commit()
    return project

def update_project(db: Session, project_id: int, owner_id: int, project_in: ProjectUpdate) -> Optional[Project]:
    project = get_project_by_id(db, project_id, owner_id)
    if project:
        data = project_in.model_dump(exclude_unset=True)
        if "title" in data:
            project.title = data["title"]
        if "description" in data:
            project.description = data["description"]
        db.commit()
        db.refresh(project)
    return project