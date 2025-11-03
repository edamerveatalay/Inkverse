from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.cruds.comment_crud import (
    create_comment_crud,
    delete_comment,
    get_comments_by_blog,
    update_comment_crud,
)
from app.database import get_session
from app.routers import blog
from app.routers.auth import get_current_user
from app.schemas.schemas_comment import (
    CommentCreate,
    CommentDelete,
    CommentRead,
    CommentUpdate,
)
from fastapi import Depends
from fastapi import status


router = APIRouter(prefix="/comment", tags=["Comments"])


@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreate,
    blog_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    new_comment = await create_comment_crud(session, comment, current_user.id, blog_id)
    return new_comment


@router.get("/", response_model=list[CommentRead])
async def get_comments_by_blog_endpoint(
    blog_id: int, session: AsyncSession = Depends(get_session)
):
    all_comment = await get_comments_by_blog(session, blog_id)
    return all_comment


@router.put("/", response_model=CommentRead)
async def update_comment_endpoint(
    comment_id: int,
    comment_update: CommentUpdate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    updated_comment = await update_comment_crud(
        session, comment_id, comment_update, current_user.id
    )
    return updated_comment


@router.delete("/", response_model=CommentRead)
async def delete_comment_endpoint(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    deleted_comment = await delete_comment(session, comment_id, current_user.id)
    return deleted_comment
