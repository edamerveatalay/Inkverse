from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class BlogCreate(BaseModel):
    title: str
    content: str
    is_published: Optional[bool] = False
    tags: list[str] = []
    image_url: Optional[str] = None


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None
    tags: Optional[list[str]] = None
    image_url: Optional[str] = None


class BlogUser(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class BlogRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    tags: list[str]
    user: Optional[BlogUser] = None
    image_url: Optional[str] = None
    likes_count: int = Field(default=0, description="Beğeni sayısı")
    is_liked: bool = Field(default=False, description="Kullanıcı beğenmiş mi?")

    class Config:
        from_attributes = True
