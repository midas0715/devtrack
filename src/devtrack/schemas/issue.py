from pydantic import BaseModel
from typing import Literal,Optional
from datetime import datetime

class IssueCreate(BaseModel):
    project_id: int
    title: str
    description: str
    assignee: Optional[str]
    status: Literal["open","in_progress","closed"]
    priority: Literal["low","medium","high"]

class IssueRead(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    assignee: Optional[str]
    status: Literal["open","in_progress","closed"]
    priority: Literal["low","medium","high"]
    creator: str
    created_at: datetime
