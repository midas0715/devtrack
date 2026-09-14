from pydantic import BaseModel
from typing import Literal,Optional
from datetime import datetime

class IssueCreate(BaseModel):
    project_id: int
    title: str
    description: str
    assignee: Optional[str]=None
    status: Literal["open","in_progress","closed"]
    priority: Literal["low","medium","high"]

class IssueRead(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    assignee: Optional[str]=None
    status: Literal["open","in_progress","closed"]
    priority: Literal["low","medium","high"]
    creator: str
    created_at: datetime

class IssueUpdate(BaseModel):
    title: Optional[str]=None
    description: Optional[str]=None
    assignee: Optional[str]=None
    status: Optional[Literal["open","in_progress","closed"]]=None
    priority: Optional[Literal["low","medium","high"]]=None