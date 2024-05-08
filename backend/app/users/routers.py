from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from . import crud, schemas, auth
from ..database import get_db  
from ..config import settings
from datetime import timedelta
from typing import List
router = APIRouter()

@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.User])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db)
    return users

@router.put("/users/{user_id}/update", response_model=schemas.User)
async def update_user_profile(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated_user = await crud.update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user_account(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = await crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User successfully deleted"}

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

@router.post("/users/{user_id}/set_vip")
async def set_user_vip(
    user_id: int,
    vip_status: bool = Query(..., description="Set VIP status of the user"),
    db: AsyncSession = Depends(get_db),
    current_admin: schemas.User = Depends(auth.get_current_admin)) -> dict:
    if not current_admin.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    updated_user = await crud.set_user_vip_status(db, user_id, vip_status)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": updated_user.username, "is_vip": updated_user.is_vip}


@router.post("/logout")
async def logout():
    return {"message": "User logged out successfully"}