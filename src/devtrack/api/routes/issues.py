from fastapi import APIRouter,Depends,HTTPException
from devtrack.schemas.issue import IssueCreate,IssueRead,IssueUpdate
from devtrack.repositories.issue_repository import get_issues,create_issue,get_issue_by_id,update_an_issue
from typing import List
from sqlalchemy.orm import Session
from devtrack.database.session import get_db

router=APIRouter()

@router.post("/issues",response_model=IssueRead)
def create_an_issue(issue:IssueCreate, db:Session=Depends(get_db)):
    return create_issue(db,issue)

@router.get("/issues",response_model=List[IssueRead])
def get_all_issues(db: Session=Depends(get_db)):
    return get_issues(db)

@router.get("/issues/{issue_id}",response_model=IssueRead)
def get_by_id(issue_id:int,db: Session=Depends(get_db)):
    issue= get_issue_by_id(db,issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail=f"Issue {issue_id} doesn't exists")
    return issue

@router.patch("/issues/{issue_id}",response_model=IssueRead)
def updating_issue(issue_id:int, update:IssueUpdate, db:Session=Depends(get_db)):
    issue = update_an_issue(db,issue_id,update)
    if issue is None:
        raise HTTPException(status_code=404, detail=f"Issue {issue_id} doesn't exists")
    return issue
