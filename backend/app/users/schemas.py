from pydantic import BaseModel, EmailStr, Field
from typing import List
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel): 
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None

class User(UserBase):
    id: int
    is_active: bool
    is_vip: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None 
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

