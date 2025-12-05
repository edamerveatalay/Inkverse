from fastapi import APIRouter, Depends, status, HTTPException
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
    # Daha önce like'lanmış mı kontrol et
    existing_like = await get_like_by_user_and_blog(
        session, user_id=current_user.id, blog_id=like.blog_id
    )

    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu blog'u zaten beğendiniz",
        )

    new_like = await create_like(session, like, current_user.id)
    return new_like


@router.get("/check", response_model=dict)
async def check_like_status(
    blog_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    like = await get_like_by_user_and_blog(
        session, user_id=current_user.id, blog_id=blog_id
    )

    return {"is_liked": like is not None, "like_id": like.id if like else None}


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_like_endpoint(
    blog_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    try:
        await delete_like(session, user_id=current_user.id, blog_id=blog_id)
        return {"message": "Beğeni kaldırıldı"}
    except HTTPException as e:
        if e.status_code == 404:
            return {"message": "Beğeni zaten kaldırılmış"}
        raise e
