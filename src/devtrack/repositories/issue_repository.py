from sqlalchemy.orm import Session
from devtrack.models.issue import Issue
from devtrack.schemas.issue import IssueCreate,IssueUpdate
from devtrack.models.user import User

def create_issue(db: Session, issue: IssueCreate, current_user: User):
    new_issue= Issue(**issue.model_dump(), creator=current_user.email)
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue

def get_issues(db: Session):
    return db.query(Issue).all()

def get_issue_by_id(db:Session, issue_id:int):
    return db.query(Issue).filter(Issue.id==issue_id).first()

def update_an_issue(db:Session, issue_id:int, updates: IssueUpdate):
    issue =db.query(Issue).filter(Issue.id==issue_id).first()
    if issue is None: return None
    update_data=updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(issue,key,value)
    db.commit()
    db.refresh(issue)
    return issue

def delete_issue(db:Session, issue_id:int):
    issue= db.query(Issue).filter(Issue.id==issue_id).first()
    if issue is None: return None
    db.delete(issue)
    db.commit()
    return issue
