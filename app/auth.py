# app/auth.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import UserCreate, UserRead, UserLogin, Token
from app.crud import create_user, get_all_users, get_user_by_email
from app.utils import verify_password, create_access_token


# GET işlemleri için router. Sign up kısmının
get_router = APIRouter(prefix="/auth", tags=["Auth - Sign Up"])


@get_router.get("/users", response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session)
    return users


# POST işlemleri için router. Sign up kısmının
post_router = APIRouter(prefix="/auth", tags=["Auth - Sign Up"])


@post_router.post(
    "/users", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
async def create_new_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    user = await create_user(session, user_data)
    return UserRead.from_orm(user)


signin_router = APIRouter(prefix="/auth/signin", tags=["Auth - Sign In"])


@signin_router.post("/", response_model=Token, status_code=status.HTTP_200_OK)
# Python decorator olarak, hemen altındaki fonksiyonu FastAPI’ye “bu bir POST endpoint” olduğunu söylemek için kullanır.


# POST isteği geldiğinde çalışacak fonksiyon
async def signin_endpoint(
    user_data: UserLogin, session: AsyncSession = Depends(get_session)
):  # endpoint
    user = await get_user_by_email(session, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")
