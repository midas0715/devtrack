from fastapi import APIRouter,Depends
from devtrack.schemas.issue import IssueCreate,IssueRead
from devtrack.repositories.issue_repository import get_issues,create_issue
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