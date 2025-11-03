from profile import Profile
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status


from app.schemas.schemas_profile import ProfileCreate, ProfileUpdate


async def create_profile(
    session: AsyncSession, profile_create: ProfileCreate, user_id: int
):

    new_profile = Profile(
        user_id=user_id,
        bio=profile_create.bio,
        profile_image=profile_create.profile_image,
        website=profile_create.website,
    )

    session.add(new_profile)
    await session.commit()
    await session.refresh(new_profile)
    return new_profile


async def get_profile_by_user(session: AsyncSession, user_id: int):
    result = await session.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalars().first()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {user_id} not found",
        )
    return profile


async def update_profile(
    session: AsyncSession, profile_update: ProfileUpdate, user_id: int
):

    result = await session.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalars().first()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {user_id} not found",
        )

    if profile_update.bio is not None:
        profile.bio = profile_update.bio

    if profile_update.profile_image is not None:
        profile.profile_image = profile_update.profile_image

    if profile_update.website is not None:
        profile.website = profile_update.website

    session.add(profile)

    await session.commit()
    await session.refresh(profile)
    return profile


async def delete_profile(session: AsyncSession, user_id: int):
    result = await session.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalars().first()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {user_id} not found",
        )
    session.delete(profile)
    await session.commit()
