from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    issue_id: int
    content: str

class CommentRead(BaseModel):
    id:int 
    issue_id: int
    content: str
    creator: str
    created_at:datetime

class CommentUpdate(BaseModel):
    content:Optional[str]=None