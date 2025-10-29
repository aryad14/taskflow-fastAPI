from sqlalchemy.orm import Session
from models.project import Project

def get_projects(db: Session, user_id: int):
    return db.query(Project).filter(Project.owner_id == user_id).all()

def create_project(db: Session, project: Project, owner_id: int):
    project = Project(**project.dict(), owner_id=owner_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_project_by_id(db: Session, project_id: int, owner_id: int):
    return db.query(Project).filter(Project.id == project_id, Project.owner_id == owner_id).first()

def delete_project(db: Session, project_id: int, owner_id: int):
    project = get_project_by_id(db, project_id, owner_id)
    if project:
        db.delete(project)
        db.commit()
    return project

def update_project(db: Session, project_id: int, owner_id: int, updated_data: dict):
    project = get_project_by_id(db, project_id, owner_id)
    if project:
        for key, value in updated_data.items():
            setattr(project, key, value)
        db.commit()
        db.refresh(project)
    return project