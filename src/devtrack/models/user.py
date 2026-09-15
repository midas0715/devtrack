from devtrack.database.base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,DateTime,func
from datetime import datetime

class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    email:Mapped[str]=mapped_column(String, unique=True)
    hashed_password:Mapped[str]=mapped_column(String) 
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())
    projects: Mapped[list["Project"]]= relationship("Project", cascade="all, delete-orphan")