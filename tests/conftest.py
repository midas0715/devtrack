from devtrack.models.project import Project
from devtrack.models.issue import Issue
from devtrack.models.comment import Comment
from devtrack.models.user import User
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from devtrack.database.base import Base
from devtrack.core.config import TEST_DATABASE_URL

engine=create_engine(TEST_DATABASE_URL)
TestingSessionLocal=sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session=TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)