from fastapi import APIRouter
from datetime import datetime
from devtrack.schemas.project import ProjectCreate,ProjectRead
from typing import List

router=APIRouter()
next_id=1
fake_db=[]

@router.post("/projects",response_model=ProjectRead)
def create_projects(project:ProjectCreate):
    global next_id
    new_item={
        "id":next_id,
        **project.model_dump(),
        "created_at":datetime.now()
    }
    fake_db.append(new_item)
    next_id+=1
    return new_item

@router.get("/projects",response_model=List[ProjectRead])
def get_projects():
    return fake_db