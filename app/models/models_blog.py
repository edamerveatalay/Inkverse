from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from app.models.models_like import Like
from sqlalchemy import Column, JSON


if TYPE_CHECKING:
    from .models_user import User
    from .models_comment import Comment


class Blog(SQLModel, table=True):
    __tablename__ = "blogs"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    is_published: bool = Field(default=False)
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))

    # ilişki tanımı
    user: Optional["User"] = Relationship(back_populates="blogs")

    comments: list["Comment"] = Relationship(
        back_populates="blog", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    likes: list["Like"] = Relationship(
        back_populates="blog", sa_relationship_kwargs={"cascade": "all, delete"}
    )
