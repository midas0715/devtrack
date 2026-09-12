from sqlalchemy.orm import Session
from devtrack.models.project import Project
from devtrack.schemas.project import ProjectCreate

def create_project(db: Session, project:ProjectCreate):
    new_project= Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_projects(db:Session):
    return db.query(Project).all()