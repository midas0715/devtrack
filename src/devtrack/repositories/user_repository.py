from devtrack.schemas.user import UserCreate,UserRead
from sqlalchemy.orm import Session
from devtrack.models.user import User
from devtrack.core.security import hash_password

def create_user(db:Session, user:UserCreate):                   
    new_user=User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email==email).first()