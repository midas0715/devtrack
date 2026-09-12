from fastapi import APIRouter,Depends
from typing import List
from devtrack.schemas.project import ProjectCreate,ProjectRead
from devtrack.database.session import get_db
from sqlalchemy.orm import Session
from devtrack.repositories.project_repository import create_project,get_projects

router=APIRouter()

@router.post("/projects",response_model=ProjectRead)
def create_projects( project: ProjectCreate, db:Session= Depends(get_db)):
    return create_project(db, project)#respository i created which store data
    

@router.get("/projects",response_model=List[ProjectRead])
def get_all_projects(db: Session=Depends(get_db)):
    return get_projects(db)