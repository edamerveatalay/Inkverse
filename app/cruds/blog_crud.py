# blog sayfalarının crud işlemleri burada olacak
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models_blog import Blog
from app.schemas.schemas_blog import BlogCreate


async def create_blog(session: AsyncSession, blog_create: BlogCreate, user_id: int):
    # BlogCreate sınıfından bir blog_create nesnesi oluşturduk onu kullanacağız kodumuzda
    blog = Blog(
        title=blog_create.title,
        user_id=user_id,  # hangi kullanıcıya ait olduğunu belirttik
        content=blog_create.content,
    )  # fonksiyonumuzun parametrelerini tanımladık

    session.add(blog)
    await session.commit()
    await session.refresh(blog)
    return blog
