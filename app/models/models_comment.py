from __future__ import annotations
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.models_blog import Blog
from app.models.models_user import User


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str  # yorum metni
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")  # iki tablo arasında bağlantı anahtarı
    blog_id: int = Field(foreign_key="blog.id")
    author: User = Relationship(
        back_populates="comments"
    )  # iki tablo arasında bağlantı kurar
    blog: Optional[Blog] = Relationship(back_populates="comments")
