from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,DateTime,func,ForeignKey
from datetime import datetime
from devtrack.database.base import Base

class Comment(Base):
    __tablename__='comments'
    id:Mapped[int]=mapped_column(primary_key=True)
    issue_id: Mapped[int]=mapped_column(ForeignKey("issues.id"),index=True)
    content: Mapped[str]=mapped_column(String)
    creator: Mapped[str]=mapped_column(String)
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now())