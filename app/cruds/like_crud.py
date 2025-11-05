from fastapi import HTTPException
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from app.models.models_like import Like
from app.schemas.schemas_like import LikeCreate


async def create_like(session: AsyncSession, like_create: LikeCreate, user_id: int):
    new_like = Like(
        user_id=user_id,
        blog_id=like_create.blog_id,
    )

    if await get_like_by_user_and_blog(session, user_id, like_create.blog_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Like already exists",
        )

    session.add(new_like)
    await session.commit()
    await session.refresh(new_like)
    return new_like


async def get_like_by_user_and_blog(session: AsyncSession, user_id: int, blog_id: int):
    result = await session.execute(
        select(Like).where(Like.user_id == user_id, Like.blog_id == blog_id)
    )
    like = result.scalars().first()
    return like


async def delete_like(session: AsyncSession, user_id: int, blog_id: int):
    result = await session.execute(
        select(Like).where(Like.user_id == user_id, Like.blog_id == blog_id)
    )
    like = result.scalars().first()
    if like is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Like not found",
        )

    session.delete(like)
    await session.commit()
