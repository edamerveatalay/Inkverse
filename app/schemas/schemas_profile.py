from typing import Optional
from pydantic import BaseModel


class ProfileCreate(BaseModel):
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    website: Optional[str] = None


class ProfileRead(BaseModel):
    id: int
    name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    website: Optional[str] = None

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    website: Optional[str] = None
