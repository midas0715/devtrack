from devtrack.repositories.project_repository import create_project
from devtrack.repositories.issue_repository import create_issue
from devtrack.repositories.comment_repository import (
    create_comment, get_comment_by_id, update_comment, delete_comment
)
from devtrack.repositories.user_repository import create_user
from devtrack.schemas.user import UserCreate
from devtrack.schemas.project import ProjectCreate
from devtrack.schemas.issue import IssueCreate
from devtrack.schemas.comment import CommentCreate, CommentUpdate

def make_test_issue(db_session):
    user = create_user(db_session, UserCreate(email="test@example.com", password="testpass"))
    project = create_project(db_session, ProjectCreate(name="Test Project", description="desc"), user)
    issue = create_issue(
        db_session,
        IssueCreate(project_id=project.id, title="Bug", description="desc", status="open", priority="low"),
        user
    )
    return user, issue

def test_create_comment(db_session):
    user, issue = make_test_issue(db_session)
    comment = create_comment(db_session, CommentCreate(issue_id=issue.id, content="Looking into it"), user)
    assert comment.id is not None
    assert comment.creator == user.email
    assert comment.issue_id == issue.id

def test_get_comment_by_id_not_found(db_session):
    assert get_comment_by_id(db_session, 99999) is None

def test_update_comment(db_session):
    user, issue = make_test_issue(db_session)
    comment = create_comment(db_session, CommentCreate(issue_id=issue.id, content="Old"), user)
    updated = update_comment(db_session, comment.id, CommentUpdate(content="New"))
    assert updated.content == "New"

def test_delete_comment(db_session):
    user, issue = make_test_issue(db_session)
    comment = create_comment(db_session, CommentCreate(issue_id=issue.id, content="Test"), user)
    delete_comment(db_session, comment.id)
    assert get_comment_by_id(db_session, comment.id) is None