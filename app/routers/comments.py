from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.cruds.comment_crud import create_comment_crud
from app.database import get_session
from app.routers.auth import get_current_user
from app.schemas.schemas_comment import (
    CommentCreate,
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
