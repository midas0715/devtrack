from devtrack.repositories.project_repository import (
    create_project, get_project_by_id, get_projects, update_project, delete_project
)
from devtrack.repositories.user_repository import create_user
from devtrack.schemas.user import UserCreate
from devtrack.schemas.project import ProjectCreate, ProjectUpdate

def make_test_user(db_session):
    user = create_user(db_session, UserCreate(email="test@example.com", password="testpass"))
    return user

def test_create_project(db_session):
    user = make_test_user(db_session)
    project = create_project(db_session, ProjectCreate(name="Test", description="desc"), user)
    assert project.id is not None
    assert project.name == "Test"
    assert project.creator_id == user.id

def test_get_project_by_id_found(db_session):
    user = make_test_user(db_session)
    created = create_project(db_session, ProjectCreate(name="Test", description="desc"), user)
    fetched = get_project_by_id(db_session, created.id)
    assert fetched.id == created.id

def test_get_project_by_id_not_found(db_session):
    result = get_project_by_id(db_session, 99999)
    assert result is None

def test_update_project(db_session):
    user = make_test_user(db_session)
    created = create_project(db_session, ProjectCreate(name="Old", description="desc"), user)
    updated = update_project(db_session, created.id, ProjectUpdate(name="New"))
    assert updated.name == "New"
    assert updated.description == "desc"  # untouched field stays the same

def test_delete_project(db_session):
    user = make_test_user(db_session)
    created = create_project(db_session, ProjectCreate(name="Test", description="desc"), user)
    delete_project(db_session, created.id)
    assert get_project_by_id(db_session, created.id) is None