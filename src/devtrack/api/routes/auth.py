from fastapi import APIRouter,Depends,HTTPException
from devtrack.repositories.user_repository import create_user,get_user_by_email
from devtrack.schemas.user import UserCreate,UserRead
from devtrack.database.session import get_db
from devtrack.core.security import verify_password,create_access_token
from sqlalchemy.orm import Session

router=APIRouter()

@router.post("/register", response_model=UserRead)
def creating_an_user(user: UserCreate, db:Session=Depends(get_db)):
    existing=get_user_by_email(db,user.email)
    if existing:
        raise HTTPException(status_code=409, detail=f"{user.email} already exists")
    return create_user(db,user)

@router.post("/login")
def user_login(cred: UserCreate, db:Session=Depends(get_db)):
    user=get_user_by_email(db,cred.email)

    if user is None or not verify_password(cred.password, user.hashed_password):
        raise HTTPException(status_code=401,detail="Incorrect email or password")

    token= create_access_token({"user_id":user.id})

    return {"access_token": token, "token_type":"bearer"}