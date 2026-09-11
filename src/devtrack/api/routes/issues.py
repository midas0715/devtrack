from fastapi import APIRouter
from devtrack.schemas.issue import IssueCreate,IssueRead
from datetime import datetime
from typing import List
next_id=1
fake_issue_db=[]
router=APIRouter()
@router.post("/issues",response_model=IssueRead)
def create_issue(issue:IssueCreate):
    global next_id
    new_issue={
        "id":next_id,
        **issue.model_dump(),
        "creator":"temp_user",
        "created_at":datetime.now()
    }
    fake_issue_db.append(new_issue)
    next_id+=1
    return new_issue
@router.get("/issues",response_model=List[IssueRead])
def get_issues():
    return fake_issue_db