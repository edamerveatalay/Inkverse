# blog endpointleri burada olacak
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas.schemas_blog import BlogCreate, BlogRead, BlogUpdate
from fastapi import Depends
from app.routers.auth import get_current_user
from app.cruds.blog_crud import (
    create_blog_crud,
    get_all_blogs,
    update_blog,
    get_my_blogs,
    delete_blog,
)
from fastapi import status

router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.post("/", response_model=BlogRead, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: BlogCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    new_blog = await create_blog_crud(session, blog, user_id=current_user.id)
    return new_blog


@router.get("/", response_model=list[BlogRead])
async def get_all_blogs_endpoint(session: AsyncSession = Depends(get_session)):
    all_blogs = await get_all_blogs(session)
    return all_blogs


@router.put("/{blog_id}", response_model=BlogRead)
async def update_blog_endpoint(
    blog_id: int,  # URL’den gelen blog ID’si.
    blog_update: BlogUpdate,
    session: AsyncSession = Depends(get_session),
    # kimin istekte bulunduğunu belirliyor.
    # Bu fonksiyon JWT token’ı çözerek şu anki kullanıcıyı bulur.
    current_user=Depends(get_current_user),
):
    updated_blog = await update_blog(session, blog_update, blog_id, current_user.id)
    return updated_blog


# Kullanıcı PUT isteği gönderir (URL + body + token)
# FastAPI endpoint parametreleri ile verileri alır:
# blog_id → URL
# blog_update → body
# current_user → token’dan get_current_user()
# Endpoint bu verileri CRUD fonksiyonuna geçirir
# CRUD fonksiyonu veritabanında gerekli güncellemeyi yapar ve sonucu döndürür
# Endpoint sonucu client’a geri yollar


@router.get("/my_blogs", response_model=list[BlogRead])
async def my_blogs(
    session: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    my_blogs_get = await get_my_blogs(session, user_id=current_user.id)
    return my_blogs_get


@router.delete("/{blog_id}", response_model=BlogRead)
async def delete_blog_endpoint(
    blog_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    deleted_blog = await delete_blog(session, user_id=current_user.id, blog_id=blog_id)
    return deleted_blog
