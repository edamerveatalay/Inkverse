from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from app.models.models_like import Like

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

    # ilişki tanımı
    user: Optional["User"] = Relationship(back_populates="blogs")

    comments: list["Comment"] = Relationship(
        back_populates="blog", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    likes: list["Like"] = Relationship(
        back_populates="blog", sa_relationship_kwargs={"cascade": "all, delete"}
    )
