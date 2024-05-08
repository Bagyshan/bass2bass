from typing import TYPE_CHECKING
from typing import Optional, List
from datetime import datetime, date, time

from pydantic import BaseModel

from pydantic import BaseModel
from typing import Optional


if TYPE_CHECKING:
    from app.users.models import User


class PostBase(BaseModel):
    title: str
    body: str
    image: str
    lat: float
    lng: float
    date: date
    time: time
    is_free: bool

    class Config:
        orm_mode = True

class PostGet(PostBase):
    id: int
    owner: str
    owner_id: int

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    owner: int

class PostUpdatePut(PostBase):
    pass


class PostUpdatePatch(PostBase):
    title: Optional[str] = None
    body: Optional[str] = None
    image: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    date: Optional[date]
    time: Optional[time]
    is_free: Optional[bool] = None



class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    posts: List[PostBase] = []

    class Config:
        orm_mode = True