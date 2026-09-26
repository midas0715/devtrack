from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,DateTime,func,ForeignKey
from datetime import datetime
from typing import Optional,Literal
from devtrack.database.base import Base

class Issue(Base):
    __tablename__="issues"
    id: Mapped[int]=mapped_column(primary_key=True)
    project_id: Mapped[int]=mapped_column(ForeignKey("projects.id"), index=True)
    title: Mapped[str]=mapped_column(String)
    description: Mapped[str]=mapped_column(String)
    assignee: Mapped[Optional[str]]=mapped_column(String, nullable=True)
    status: Mapped[str]=mapped_column(String)
    priority: Mapped[str]=mapped_column(String)
    creator: Mapped[str]=mapped_column(String)
    created_at: Mapped[datetime]=mapped_column(DateTime,server_default=func.now())
    comments: Mapped[list["Comment"]] = relationship("Comment", cascade="all, delete-orphan")