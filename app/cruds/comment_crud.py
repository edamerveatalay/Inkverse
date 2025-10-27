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


async def get_comments_by_blog(session: AsyncSession, blog_id: int):
    result = await session.execute(select(Comment).where(Comment.blog_id == blog_id))
    comments = result.scalars().all()
    return comments


async def delete_comment(
    session: AsyncSession, comment_id: int, user_id: int
):  # yorumun id'si olduğu için nereye yazıldığı belli blog_id'ye gerek yok
    result = await session.execute(select(Comment).where(Comment.id == comment_id))
    # veritabanında comment_id ile eşleşen satırları arama işlevi görür.
    comment = result.scalars().first()

    if comment is None:  # id boşsa veritabanında o id'de bir id bulunamadı demek
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {comment_id} not found",
        )
    if (
        comment.user_id != user_id
    ):  # silinecek yorum şu anki kullanıcının mı diye kontrol ediyoruz. başkasının yorumunun silinmesi engelleniyor
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this comment",
        )

    await session.delete(comment)
    await session.commit()  # Commit ile değişiklik veritabanına uygulanır.
    return comment


async def update_comment_crud(
    session: AsyncSession, comment_id: int, user_id: int, comment_update: CommentUpdate
):
    result = await session.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalars().first()

    if comment is None:  # id boşsa veritabanında o id'de bir id bulunamadı demek
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {comment_id} not found",
        )
    if comment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this comment",
        )

    session.add(comment)
    comment.content = comment_update.content
    await session.commit()
    await session.refresh(comment)
    return comment
