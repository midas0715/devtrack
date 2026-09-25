from fastapi import APIRouter,Depends,HTTPException
from typing import List
from devtrack.schemas.project import ProjectCreate,ProjectRead,ProjectUpdate
from devtrack.database.session import get_db
from sqlalchemy.orm import Session
from devtrack.repositories.project_repository import create_project,get_projects,get_project_by_id,update_project,delete_project
from devtrack.models.user import User
from devtrack.api.dependencies import get_current_user
import json
from devtrack.core.redis_client import redis_client
from devtrack.core.cache import build_cache_key,invalidate_projects_cache

router=APIRouter()

@router.post("/projects",response_model=ProjectRead)
def create_projects(project: ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    result = create_project(db, project, user)
    invalidate_projects_cache()
    return result
    

@router.get("/projects",response_model=List[ProjectRead])
def get_all_projects(search:str=None,limit:int=20,offset:int=0,db: Session=Depends(get_db)):
    cache_key= build_cache_key(search,limit,offset)

    cached= redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    projects = get_projects(db, search, limit, offset)
    result = [ProjectRead.model_validate(p).model_dump(mode="json") for p in projects]

    redis_client.set(cache_key, json.dumps(result), ex=60)

    return result

@router.get("/projects/{project_id}", response_model=ProjectRead)
def get_by_id(project_id:int,db:Session=Depends(get_db)):
    project= get_project_by_id(db,project_id)
    if project is None: 
        raise HTTPException(status_code=404,detail=f"Project {project_id} not found")
    return project

@router.patch("/projects/{project_id}", response_model=ProjectRead)
def updating_project(project_id: int, updates: ProjectUpdate, db: Session= Depends(get_db)):
    project= update_project(db,project_id,updates)
    if project is None:
        raise HTTPException(status_code=404,detail=f"Project {project_id} not found")
    return project

@router.delete("/projects/{project_id}", status_code=204)
def deleting_a_project(project_id:int, db:Session= Depends(get_db)):
    project= delete_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project {project_id} doesn't exists")
    return project