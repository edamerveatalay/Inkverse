from fastapi import APIRouter, Depends

from app.cruds.profile_crud import (
    create_profile,
    delete_profile,
    get_profile_by_user,
    update_profile,
)
from app.routers.auth import get_current_user
from app.schemas.schemas_profile import ProfileCreate, ProfileRead, ProfileUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session

from fastapi import status

router = APIRouter(prefix="/profile", tags=["Profiles"])


@router.post("/", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile_endpoint(
    profile: ProfileCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    new_profile = await create_profile(session, profile, user_id=current_user.id)
    return new_profile


@router.get("/", response_model=ProfileRead)
async def get_profile_by_user_endpoint(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    by_profile = await get_profile_by_user(session, current_user.id)

    # Eğer profil yoksa otomatik oluştur
    if not by_profile:
        new_profile = await create_profile(
            session,
            ProfileCreate(bio="", profile_image="", website="", name=""),
            user_id=current_user.id,
        )
        return new_profile

    return by_profile


@router.put(
    "/", response_model=ProfileRead
)  # göndürülem(dönen) veriyi belirtir response_model
async def update_profile_endpoint(
    profile: ProfileUpdate,  # kullanıcıdan gelen veri. güvenlik amacıyla gelen veri ve dönen veri farklı oluyor
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    updated_profile = await update_profile(session, profile, current_user.id)
    return updated_profile


@router.delete("/", response_model=ProfileRead)
async def delete_profile_endpoint(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):

    deleted_profile = await delete_profile(session, current_user.id)
    return deleted_profile
