# blog endpointleri burada olacak
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas.schemas_blog import BlogCreate, BlogRead, BlogUpdate
from fastapi import Depends
from app.routers.auth import get_current_user
from app.cruds.blog_crud import create_blog
from fastapi import status

router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.post("/", response_model=BlogRead, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: BlogCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    new_blog = await create_blog(session, blog, user_id=current_user.id)
    return new_blog
