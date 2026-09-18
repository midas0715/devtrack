from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from devtrack.repositories.user_repository import create_user,get_user_by_email
from devtrack.schemas.user import UserCreate,UserRead
from devtrack.database.session import get_db
from devtrack.core.security import verify_password,create_access_token
from sqlalchemy.orm import Session

router=APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserRead)
def creating_an_user(user: UserCreate, db:Session=Depends(get_db)):
    existing=get_user_by_email(db,user.email)
    if existing:
        raise HTTPException(status_code=409, detail=f"{user.email} already exists")
    return create_user(db,user)

@router.post("/login")
def user_login(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=get_user_by_email(db,form_data.username)

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401,detail="Incorrect email or password")

    token= create_access_token({"user_id":user.id})

    return {"access_token": token, "token_type":"bearer"}

from devtrack.api.dependencies import get_current_user
from devtrack.models.user import User
@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}