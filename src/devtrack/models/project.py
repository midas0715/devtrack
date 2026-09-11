from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,DateTime,func
from datetime import datetime
from typing import Optional
from devtrack.database.base import Base

class Project(Base):
    __tablename__="projects"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String)
    description: Mapped[Optional[str]]=mapped_column(String, nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())