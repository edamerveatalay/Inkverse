from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserCreate, UserRead
from app.crud import create_user
from app.database import get_session  # session için

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup", response_model=list[UserRead], status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await create_user(session, user_data)
    return [UserRead.from_orm(user)]
