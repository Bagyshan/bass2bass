
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
import json
from datetime import datetime, date, time
from typing import List, Optional
from .schemas import PostBase
from .models import Post, Category
from . import schemas, models
from ..database import scoped_session_dependency


async def create_post(
        session: AsyncSession, 
        post: schemas.PostBase,
        current_user_id: int,
    ) -> schemas.PostCreate:
    post_data = post.dict()
    post_data["owner"] = current_user_id
    post_data["date"] = date.fromisoformat(str(post_data["date"]))
    post_data["time"] = time.fromisoformat(str(post_data["time"]))
    post = Post(**post_data)
    session.add(post)
    await session.commit()
    return post

async def get_post(session: AsyncSession, post_id: int) -> dict | None:
    stmt = select(Post).options(joinedload(Post.owner_details)).filter(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post = result.scalar()

    if post is not None:
        post_dict = {
            "id": post.id,
            "owner": post.owner_details.username,
            "owner_id": post.owner_details.id,
            "title": post.title, 
            "body": post.body, 
            "image": post.image, 
            "date": post.date,
            "time": post.time, 
            "is_free": post.is_free,
            "lat": post.lat, 
            "lng": post.lng, 
        }
        return post_dict
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )


async def get_posts(session: AsyncSession) -> list[dict]:
    stmt = select(Post).options(joinedload(Post.owner_details)).order_by(Post.id)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return [
        {
            "id": post.id, 
            "owner": post.owner_details.username, 
            "owner_id": post.owner_details.id, 
            "title": post.title, 
            "body": post.body, 
            "image": post.image, 
            "date": post.date,
            "time": post.time, 
            "is_free": post.is_free,
            "lat": post.lat, 
            "lng": post.lng, 
        } for post in posts
    ]




async def update_post(
        session: AsyncSession,
        post_id: int,
        post_update: schemas.PostUpdatePatch,
        current_user_id: int,
    ) -> schemas.PostCreate:
    stmt = select(Post).filter(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post = result.scalar()
    if post.owner != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="It's not your post"
        )

    if post is not None:
        post_data = post_update.dict(exclude_unset=True)
        post_data["date"] = date.fromisoformat(str(post_data["date"]))
        post_data["time"] = time.fromisoformat(str(post_data["time"]))
        for key, value in post_data.items():
            setattr(post, key, value)
        await session.commit()
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )


async def delete_post(
        session: AsyncSession, 
        post_id: int, 
        current_user_id: int
    ) -> str:
    stmt = select(Post).filter(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post = result.scalar()

    if post.owner != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="It's not your post"
        )
    
    if post is not None:
        await session.delete(post)
        await session.commit()
        return "Post deleted successfully"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    


async def create_category(db: AsyncSession, category: schemas.CategoryCreate) -> models.Category:
    db_category = models.Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_categories(db: AsyncSession) -> List[models.Category]:
    async with db:
        result = await db.execute(select(models.Category))
        categories = result.scalars().all()
    return categories

async def update_category(db: AsyncSession, category_id: int, category_data: schemas.CategoryCreate) -> models.Category:
    async with db:
        result = await db.execute(select(models.Category).where(models.Category.id == category_id))
        category = result.scalar()
        if category:
            for key, value in category_data.dict().items():
                setattr(category, key, value)
            await db.commit()
            await db.refresh(category)
            return category
        else:
            raise HTTPException(status_code=404, detail="Category not found")

async def delete_category(db: AsyncSession, category_id: int) -> None:
    async with db:
        result = await db.execute(select(models.Category).where(models.Category.id == category_id))
        category = result.scalar()
        if category:
            await db.delete(category)
            await db.commit()
        else:
            raise HTTPException(status_code=404, detail="Category not found")
        
async def get_posts_by_dates(session: AsyncSession, dates: date) -> list[dict] | None:
    query = select(Post).options(joinedload(Post.owner_details)).filter(Post.date == dates)
    result = await session.execute(query)
    posts = result.scalars().all()
    return [
        {
            "id": post.id, 
            "owner": post.owner_details.username, 
            "owner_id": post.owner_details.id, 
            "title": post.title, 
            "body": post.body, 
            "image": post.image, 
            "date": post.date,
            "time": post.time, 
            "is_free": post.is_free,
            "lat": post.lat, 
            "lng": post.lng, 
        } for post in posts
    ]