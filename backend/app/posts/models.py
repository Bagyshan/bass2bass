
from typing import TYPE_CHECKING
from datetime import datetime, date, time
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from sqlalchemy import String, Text, Column, Integer

if TYPE_CHECKING:
    from app.users.models import User


class Post(Base):
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")
    image: Mapped[str] = mapped_column(Text, default="", server_default="")
    owner: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    lat: Mapped[float]
    lng: Mapped[float]
    date: Mapped[date]
    time: Mapped[time]
    is_free: Mapped[bool]
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='posts')
    owner_details: Mapped["User"] = relationship("User", back_populates='posts')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    posts = relationship('Post', back_populates='category')