from sqlalchemy.orm import Session
from devtrack.models.issue import Issue
from devtrack.schemas.issue import IssueCreate

def create_issue(db: Session, issue: IssueCreate):
    new_issue= Issue(**issue.model_dump(), creator="temp_user")
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue

def get_issues(db: Session):
    return db.query(Issue).all()

def get_issue_by_id(db:Session, issue_id:int):
    return db.query(Issue).filter(Issue.id==issue_id).first()