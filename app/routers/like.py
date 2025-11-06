from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.like_crud import create_like, delete_like, get_like_by_user_and_blog
from app.database import get_session
from app.routers.auth import get_current_user
from app.schemas.schemas_like import LikeCreate, LikeRead

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/", response_model=LikeRead, status_code=status.HTTP_201_CREATED)
async def create_like_endpoint(
    like: LikeCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    blog_id = like.blog_id  # hangi blog beğeniliyor
    user_id = current_user.id  # beğenen kullanıcı
    new_like = await create_like(session, like, current_user.id)
    return new_like


@router.get("/", response_model=LikeRead, status_code=status.HTTP_200_OK)
async def check_like_status(  # hangi blogun beğenildiğini kontrol et
    blog_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    like = await get_like_by_user_and_blog(
        session, blog_id=blog_id, user_id=current_user.id
    )
    return like


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like_endpoint(
    blog_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    user_id = current_user.id
    deleted_like = await delete_like(session, user_id=current_user.id, blog_id=blog_id)
    return deleted_like
