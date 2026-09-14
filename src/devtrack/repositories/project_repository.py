from sqlalchemy.orm import Session
from devtrack.models.project import Project
from devtrack.schemas.project import ProjectCreate,ProjectUpdate

def create_project(db: Session, project:ProjectCreate):
    new_project= Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_projects(db:Session):
    return db.query(Project).all()

def get_project_by_id(db:Session, project_id:int):
    return db.query(Project).filter(Project.id==project_id).first()

def update_project(db: Session, project_id:int, updates: ProjectUpdate):
    project = db.query(Project).filter(Project.id==project_id).first()
    if project is None: return None
    update_data=updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project,key,value)
    db.commit()
    db.refresh(project)
    return project