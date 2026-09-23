from devtrack.repositories.project_repository import create_project
from devtrack.repositories.issue_repository import (
    create_issue, get_issue_by_id, update_an_issue, delete_issue
)
from devtrack.repositories.user_repository import create_user
from devtrack.schemas.user import UserCreate
from devtrack.schemas.project import ProjectCreate
from devtrack.schemas.issue import IssueCreate, IssueUpdate

def make_test_user(db_session):
    return create_user(db_session, UserCreate(email="test@example.com", password="testpass"))

def make_test_project(db_session, user):
    return create_project(db_session, ProjectCreate(name="Test Project", description="desc"), user)

def test_create_issue(db_session):
    user = make_test_user(db_session)
    project = make_test_project(db_session, user)
    issue = create_issue(
        db_session,
        IssueCreate(project_id=project.id, title="Bug", description="desc", status="open", priority="low"),
        user
    )
    assert issue.id is not None
    assert issue.creator == user.email
    assert issue.project_id == project.id

def test_get_issue_by_id_not_found(db_session):
    assert get_issue_by_id(db_session, 99999) is None

def test_update_issue(db_session):
    user = make_test_user(db_session)
    project = make_test_project(db_session, user)
    issue = create_issue(
        db_session,
        IssueCreate(project_id=project.id, title="Bug", description="desc", status="open", priority="low"),
        user
    )
    updated = update_an_issue(db_session, issue.id, IssueUpdate(status="closed"))
    assert updated.status == "closed"
    assert updated.title == "Bug"  # untouched field stays the same

def test_delete_issue(db_session):
    user = make_test_user(db_session)
    project = make_test_project(db_session, user)
    issue = create_issue(
        db_session,
        IssueCreate(project_id=project.id, title="Bug", description="desc", status="open", priority="low"),
        user
    )
    delete_issue(db_session, issue.id)
    assert get_issue_by_id(db_session, issue.id) is None