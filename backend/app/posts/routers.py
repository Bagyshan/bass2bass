from fastapi import APIRouter, HTTPException, status, Depends, Query
from .models import Post
from .schemas import PostBase, PostCreate, PostUpdatePut, PostGet, PostUpdatePatch
from ..database import scoped_session_dependency
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas
from app.users.models import User   
from app.users.auth import get_current_admin
from .dependencies import get_current_vip_user, post_by_id
from . import models
from typing import List, Optional
from ..database import get_db
from datetime import date
router = APIRouter(prefix='/post', tags=['posts'])

@router.post(
    "/",
    response_model=PostCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post_in: PostBase,
    session: AsyncSession = Depends(scoped_session_dependency),
    current_user: User = Depends(get_current_vip_user)
):
    current_user_id = current_user.id
    return await crud.create_post(
        session=session, 
        post=post_in,
        current_user_id=current_user_id
    )


@router.get("/", response_model=list[PostGet])
async def get_posts(
    dates: date = None,
    session: AsyncSession = Depends(scoped_session_dependency),
) -> List[PostGet]:
    if dates:
        return await crud.get_posts_by_dates(session=session, dates=dates)
    return await crud.get_posts(session=session)


@router.get("/{post_id}/", response_model=PostGet)
async def get_post(
    post: Post = Depends(post_by_id),
) -> PostGet:
    return post



@router.put("/{post_id}/", response_model=PostUpdatePut)
async def put_update_post(
    post_id: int,
    post_update: PostUpdatePut,
    session: AsyncSession = Depends(scoped_session_dependency),
    current_user_id: User = Depends(get_current_vip_user),
) -> PostUpdatePut:
    user_id = current_user_id.id
    return await crud.update_post(
        session=session, 
        post_id=post_id, 
        post_update=post_update, 
        current_user_id=user_id
    )


@router.patch("/{post_id}/", response_model=PostUpdatePatch)
async def patch_update_post(
    post_id: int,
    post_update: PostUpdatePatch,
    session: AsyncSession = Depends(scoped_session_dependency),
    current_user_id: User = Depends(get_current_vip_user),
) -> PostUpdatePatch:
    user_id = current_user_id.id
    return await crud.update_post(
        session=session, 
        post_id=post_id, 
        post_update=post_update, 
        current_user_id=user_id
    )


@router.delete("/{post_id}/", response_model=str)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(scoped_session_dependency),
    current_user_id: User = Depends(get_current_vip_user),
) -> str:
    user_id = current_user_id.id
    return await crud.delete_post(session=session, post_id=post_id, current_user_id=user_id)


@router.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return await crud.create_category(db=db, category=category)

@router.get("/categories/", response_model=List[schemas.Category])
async def read_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db=db)

@router.put("/categories/{category_id}/", response_model=schemas.Category)
async def update_category(category_id: int, category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return await crud.update_category(db=db, category_id=category_id, category_data=category)

@router.delete("/categories/{category_id}/")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    await crud.delete_category(db=db, category_id=category_id)
    return {"detail": "Category deleted successfully"}


@router.get("/", response_model=List[PostGet])
async def get_posts_by_dates(
    dates: date,
    session: AsyncSession = Depends(scoped_session_dependency),
) -> List[PostGet]:
    return await crud.get_posts_by_dates(session=session, dates=dates)