from fastapi import APIRouter,Depends,HTTPException
from devtrack.repositories.user_repository import create_user,get_user_by_email
from devtrack.schemas.user import UserCreate,UserRead
from devtrack.database.session import get_db
from sqlalchemy.orm import Session

router=APIRouter()

@router.post("/register", response_model=UserRead)
def creating_an_user(user: UserCreate, db:Session=Depends(get_db)):
    existing=get_user_by_email(db,user.email)
    if existing:
        raise HTTPException(status_code=409, detail=f"{user.email} already exists")
    return create_user(db,user)

