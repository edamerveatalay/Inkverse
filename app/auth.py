# app/auth.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import UserCreate, UserRead
from app.crud import create_user, get_all_users


# 🔹 GET işlemleri için router
get_router = APIRouter(
    prefix="/auth",
    tags=["Auth - GET"]
)

@get_router.get("/users", response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session)
    return users


# 🔹 POST işlemleri için router
post_router = APIRouter(
    prefix="/auth",
    tags=["Auth - POST"]
)

@post_router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await create_user(session, user_data)
    return UserRead.from_orm(user)
