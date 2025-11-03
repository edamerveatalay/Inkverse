# istemci ile iletişime geçecek pydantic şemaları
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str


class CommentRead(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    blog_id: int
    author: Optional[str] = None

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True
