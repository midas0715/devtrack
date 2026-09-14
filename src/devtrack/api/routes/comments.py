from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from devtrack.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from devtrack.database.session import get_db
from devtrack.repositories.comment_repository import (
    create_comment, get_comments, get_comment_by_id, update_comment, delete_comment
)

router = APIRouter()

@router.post("/comments", response_model=CommentRead)
def create_a_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db, comment)

@router.get("/comments", response_model=List[CommentRead])
def get_all_comments(db: Session = Depends(get_db)):
    return get_comments(db)

@router.get("/comments/{comment_id}", response_model=CommentRead)
def get_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment = get_comment_by_id(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail=f"Comment {comment_id} not found")
    return comment

@router.patch("/comments/{comment_id}", response_model=CommentRead)
def updating_comment(comment_id: int, updates: CommentUpdate, db: Session = Depends(get_db)):
    comment = update_comment(db, comment_id, updates)
    if comment is None:
        raise HTTPException(status_code=404, detail=f"Comment {comment_id} not found")
    return comment

@router.delete("/comments/{comment_id}", status_code=204)
def deleting_a_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = delete_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail=f"Comment {comment_id} not found")