from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user(db: AsyncSession, username: str):
    async with db as session:
        result = await session.execute(select(models.User).filter(models.User.username == username))
        return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=fake_hashed_password)
    async with db as session:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

async def set_user_vip_status(db: AsyncSession, user_id: int, vip_status: bool):
    async with db.begin():
        stmt = select(models.User).where(models.User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if user:
            user.is_vip = vip_status
            await db.commit()
            return user
    return None

async def get_users(db: AsyncSession):
    async with db as session:
        result = await session.execute(select(models.User))
        users = result.scalars().all()
        return users
    
async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate):
    async with db as session:
        result = await session.execute(select(models.User).filter(models.User.id == user_id))
        user = result.scalars().first()
        if user:
            user_data = user_update.dict(exclude_unset=True)
            for key, value in user_data.items():
                setattr(user, key, value)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        
async def delete_user(db: AsyncSession, user_id: int):
    async with db.begin():
        stmt = select(models.User).where(models.User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()
            return True
    return False