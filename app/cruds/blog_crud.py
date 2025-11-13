# blog sayfalarının crud işlemleri burada olacak
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models_blog import Blog
from app.schemas.schemas_blog import BlogCreate, BlogUpdate
from fastapi import HTTPException, status


async def create_blog_crud(
    session: AsyncSession, blog_create: BlogCreate, user_id: int
):
    # BlogCreate sınıfından bir blog_create nesnesi oluşturduk onu kullanacağız kodumuzda
    blog = Blog(
        title=blog_create.title,
        user_id=user_id,  # hangi kullanıcıya ait olduğunu belirttik
        content=blog_create.content,
        is_published=False,
    )  # fonksiyonumuzun parametrelerini tanımladık

    session.add(blog)
    await session.commit()
    await session.refresh(blog)
    return blog


async def get_all_blogs(session: AsyncSession):
    # veri almıyor yalnızca veri okuyor o yüzden veritabanı bağlantısı yeterli
    result = await session.execute(select(Blog))
    # veritabanına SELECT * FROM blog komutunu gönder ve sonucu al
    blogs = result.scalars().all()  # Tüm blog nesnelerini al
    return blogs
    # Önce result değişkenine select * from blog yani Blog tablosundaki tüm verileri seçme sorgusu çalıştırılıp sonucu atıyoruz, sonra scalars() ile her satırdaki Blog nesnelerini çıkarıyoruz ve all() ile tablodaki tüm Blog nesnelerini liste olarak döndürüyoruz.
    # blog nesneleri blog sınıfında bulunan veriler yani id, content, title gibi


async def update_blog(
    session: AsyncSession, blog_update: BlogUpdate, blog_id: int, user_id: int
):
    result = await session.execute(
        select(Blog).where(Blog.id == blog_id)
    )  # Blog sınıfındaki id alanına bu blog'un idsini eşitledik
    # güncelleme istenen blog id'si veritabanındaki blog id'siyle eşleşiyorsa:
    # Blog tablosundaki verileri seç bu id'deki veriyi göster.
    blog = result.scalars().first()
    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )
    session.add(blog)
    blog.title = blog_update.title
    blog.content = blog_update.content
    # Veritabanından eşleşen blogu aldık ve blog_update içindeki yeni verileri mevcut blog nesnesine atadık
    await session.commit()
    await session.refresh(blog)
    return blog


async def get_my_blogs(session: AsyncSession, user_id: int):
    result = await session.execute(select(Blog).where(Blog.user_id == user_id))
    blogs = result.scalars().all()
    return blogs


async def delete_blog(session: AsyncSession, user_id: int, blog_id: int):
    result = await session.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalars().first()
    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )
    if blog.user_id != user_id:
        # Bu blogu silmek isteyen kullanıcının (user_id) kimliği, blogun sahibinin (blog.user_id) kimliğiyle aynı mı diye kontrol
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this blog",
        )

    await session.delete(blog)
    await session.commit()
    return blog
