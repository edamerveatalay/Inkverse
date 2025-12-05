import os
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models.models_blog import Blog
from app.models.models_like import Like
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
    current_user=Depends(get_current_user),
    is_published: Optional[bool] = None,
):
    # Temel sorgu
    query = select(Blog).options(selectinload(Blog.user))

    # Filtreleme
    if is_published is None:
        query = query.where(Blog.is_published == True)
    else:
        query = query.where(Blog.is_published == is_published)

    result = await session.execute(query)
    blogs = result.scalars().all()

    # Her blog için like bilgilerini hesapla
    blogs_with_likes = []
    for blog in blogs:
        # Like sayısını hesapla
        likes_count_stmt = select(func.count()).where(Like.blog_id == blog.id)
        likes_count_result = await session.execute(likes_count_stmt)
        likes_count = likes_count_result.scalar() or 0

        # Kullanıcı bu blog'u beğenmiş mi?
        is_liked = False
        if current_user:
            like_check_stmt = select(Like).where(
                Like.blog_id == blog.id, Like.user_id == current_user.id
            )
            like_check_result = await session.execute(like_check_stmt)
            is_liked = like_check_result.scalar_one_or_none() is not None

        # Blog objesini dictionary'e çevir
        blog_dict = {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "created_at": blog.created_at,
            "updated_at": blog.updated_at,
            "user_id": blog.user_id,
            "tags": blog.tags or [],
            "image_url": blog.image_url,
            "is_published": blog.is_published,
            "user": (
                {
                    "id": blog.user.id,
                    "username": blog.user.username,
                }
                if blog.user
                else None
            ),
            "likes_count": likes_count,
            "is_liked": is_liked,
        }

        blogs_with_likes.append(blog_dict)

    return blogs_with_likes


@router.get("/{blog_id}", response_model=BlogRead)
async def get_blog_detail(
    blog_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    # Blog'u getir
    query = select(Blog).where(Blog.id == blog_id).options(selectinload(Blog.user))
    result = await session.execute(query)
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog bulunamadı")

    # Like sayısını hesapla
    likes_count_stmt = select(func.count()).where(Like.blog_id == blog.id)
    likes_count_result = await session.execute(likes_count_stmt)
    likes_count = likes_count_result.scalar() or 0

    # Kullanıcı bu blog'u beğenmiş mi?
    is_liked = False
    if current_user:
        like_check_stmt = select(Like).where(
            Like.blog_id == blog.id, Like.user_id == current_user.id
        )
        like_check_result = await session.execute(like_check_stmt)
        is_liked = like_check_result.scalar_one_or_none() is not None

    # Response'u hazırla
    blog_dict = {
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "created_at": blog.created_at,
        "updated_at": blog.updated_at,
        "user_id": blog.user_id,
        "tags": blog.tags or [],
        "image_url": blog.image_url,
        "is_published": blog.is_published,
        "user": (
            {
                "id": blog.user.id,
                "username": blog.user.username,
            }
            if blog.user
            else None
        ),
        "likes_count": likes_count,
        "is_liked": is_liked,
    }

    return blog_dict


@router.put("/{blog_id}", response_model=BlogRead)
async def update_blog_endpoint(
    blog_id: int,
    blog_update: BlogUpdate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    updated_blog = await update_blog(
        session=session,
        blog_update=blog_update,
        blog_id=blog_id,
        user_id=current_user.id,
    )

    # Güncellenmiş blog için like bilgilerini getir
    return await get_blog_detail(blog_id, session, current_user)


@router.delete("/{blog_id}", response_model=BlogRead)
async def delete_blog_endpoint(
    blog_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    deleted_blog = await delete_blog(session, user_id=current_user.id, blog_id=blog_id)
    return deleted_blog


@router.post("/{blog_id}/publish", response_model=BlogRead)
async def publish_blog(
    blog_id: int,
    blog_update: BlogUpdate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await session.execute(
        select(Blog).where(Blog.id == blog_id, Blog.user_id == current_user.id)
    )
    blog = result.scalars().first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog bulunamadı")

    if blog_update.title is not None:
        blog.title = blog_update.title
    if blog_update.content is not None:
        blog.content = blog_update.content
    if blog_update.tags is not None:
        blog.tags = blog_update.tags
    if blog_update.image_url is not None:
        blog.image_url = blog_update.image_url

    blog.is_published = True

    await session.commit()
    await session.refresh(blog)

    # Yayınlanmış blog için like bilgilerini getir
    return await get_blog_detail(blog_id, session, current_user)


@router.get("/drafts", response_model=list[BlogRead])
async def get_drafts(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await session.execute(
        select(Blog)
        .where(Blog.is_published == False, Blog.user_id == current_user.id)
        .order_by(Blog.created_at.desc())
        .options(selectinload(Blog.user))
    )

    blogs = result.scalars().all()

    # Draft'lar için de like bilgilerini hesapla
    blogs_with_likes = []
    for blog in blogs:
        # Like sayısını hesapla
        likes_count_stmt = select(func.count()).where(Like.blog_id == blog.id)
        likes_count_result = await session.execute(likes_count_stmt)
        likes_count = likes_count_result.scalar() or 0

        # Kullanıcı bu blog'u beğenmiş mi? (draft'ları genelde sadece sahibi görür)
        is_liked = False
        like_check_stmt = select(Like).where(
            Like.blog_id == blog.id, Like.user_id == current_user.id
        )
        like_check_result = await session.execute(like_check_stmt)
        is_liked = like_check_result.scalar_one_or_none() is not None

        blog_dict = {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "created_at": blog.created_at,
            "updated_at": blog.updated_at,
            "user_id": blog.user_id,
            "tags": blog.tags or [],
            "image_url": blog.image_url,
            "is_published": blog.is_published,
            "user": (
                {
                    "id": blog.user.id,
                    "username": blog.user.username,
                }
                if blog.user
                else None
            ),
            "likes_count": likes_count,
            "is_liked": is_liked,
        }

        blogs_with_likes.append(blog_dict)

    return blogs_with_likes
