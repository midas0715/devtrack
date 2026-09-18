from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from devtrack.core.config import DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal= sessionmaker(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()