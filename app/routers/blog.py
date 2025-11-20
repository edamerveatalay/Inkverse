# blog endpointleri burada olacak
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_session
from app.models.models_blog import Blog
from app.schemas.schemas_blog import BlogCreate, BlogRead, BlogUpdate
from app.routers.auth import get_current_user
from app.cruds.blog_crud import (
    create_blog_crud,
    get_all_blogs,
    update_blog,
    get_my_blogs,
    delete_blog,
)

router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.post("/", response_model=BlogRead, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: BlogCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    new_blog = await create_blog_crud(
        session,
        blog,
        user_id=current_user.id,
        is_published=getattr(blog, "is_published", False),
    )
    return new_blog


@router.get("/", response_model=list[BlogRead])
async def get_all_blogs_endpoint(
    session: AsyncSession = Depends(get_session),
    is_published: Optional[bool] = None,
):
    query = select(Blog)

    # Varsayılan davranış: sadece yayınlanmış blogları getir
    if is_published is None:
        query = query.where(Blog.is_published == True)
    else:
        query = query.where(Blog.is_published == is_published)

    result = await session.execute(query)
    return result.scalars().all()


@router.put("/{blog_id}", response_model=BlogRead)
async def update_blog_endpoint(
    blog_id: int,
    blog_update: BlogUpdate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    updated_blog = await update_blog(session, blog_update, blog_id, current_user.id)
    return updated_blog


@router.get("/my_blogs", response_model=list[BlogRead])
async def my_blogs(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
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


@router.post(
    "/{blog_id}/publish", response_model=BlogRead, status_code=status.HTTP_200_OK
)
async def publish_blog(
    blog_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await session.execute(
        select(Blog).where(Blog.id == blog_id, Blog.user_id == current_user.id)
    )
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog bulunamadı")
    if blog.is_published:
        raise HTTPException(status_code=400, detail="Blog zaten yayınlanmış")

    blog.is_published = True
    await session.commit()
    await session.refresh(blog)
    return blog


@router.get("/drafts", response_model=list[BlogRead])
async def get_drafts(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await session.execute(
        select(Blog)
        .where(Blog.is_published == False, Blog.user_id == current_user.id)
        .order_by(Blog.created_at.desc())
    )

    return result.scalars().all()
