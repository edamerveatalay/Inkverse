from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models_blog import Blog
from app.models.models_comment import Comment
from app.schemas.schemas_comment import CommentCreate, CommentRead, CommentUpdate
from fastapi import HTTPException, status


async def create_comment_crud(
    session: AsyncSession, comment_create: CommentCreate, user_id: int, blog_id: int
):
    result = await session.execute(
        select(Blog).where(Blog.id == blog_id)
    )  # yorum yapılmak istenen blog var mı kontrol
    blog = (
        result.scalars().first()
    )  # veritabanındaki o id'ye sahip blog alınıp buna yorum eklenecek demek
    if blog is None:  # id boşsa veritabanında o id'de bir id bulunamadı demek
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )
    comment = Comment(content=comment_create.content, blog_id=blog_id, user_id=user_id)
    await session.add()
    await session.commit()
    await session.refresh(comment)
    return comment
