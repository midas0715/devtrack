
from sqlalchemy.orm import Session
from devtrack.models.comment import Comment
from devtrack.schemas.comment import CommentCreate, CommentUpdate
from devtrack.models.user import User

def create_comment(db: Session, comment: CommentCreate, user: User):
    new_comment = Comment(**comment.model_dump(), creator=user.email)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_comments(db: Session):
    return db.query(Comment).all()

def get_comment_by_id(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def update_comment(db: Session, comment_id: int, updates: CommentUpdate):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        return None
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(comment, key, value)
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        return None
    db.delete(comment)
    db.commit()
    return comment
