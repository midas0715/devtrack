from pydantic import BaseModel,EmailStr, field_validator
from datetime import datetime
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        return value.lower()


class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime