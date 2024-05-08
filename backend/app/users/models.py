from sqlalchemy import Column, Integer, String, Boolean

from ..database import Base
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.posts.models import Post

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_vip = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)  
    first_name = Column(String, index=True)  
    last_name = Column(String, index=True)   
    
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="owner_details")