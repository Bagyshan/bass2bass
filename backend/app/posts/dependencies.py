from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path
from typing import Annotated, Optional
from app.users.crud import get_user
from app.users.auth import oauth2_scheme
from app.users.models import User
from .crud import get_post
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..database import get_db, scoped_session_dependency
from .models import Post
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

SECRET_KEY = "hjvx blju bnxv jovh"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



async def get_current_vip_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    vip_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You couldn't create post if you have not a VIP status",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = await get_user(db, username=username)
        if user.is_vip == False:
            raise vip_credentials_exception
    except JWTError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user


async def post_by_id(
    post_id: Annotated[int, Path],
    session: AsyncSession = Depends(scoped_session_dependency),
) -> Post:
    post = await get_post(session=session, post_id=post_id)
    if post is not None:
        return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found!"
    )