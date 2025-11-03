from typing import Optional
from pydantic import BaseModel


class ProfileCreate(BaseModel):
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    website: Optional[str] = None


class ProfileRead(BaseModel):
    id: int
    email: str
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    website: Optional[str] = None

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    website: Optional[str] = None
