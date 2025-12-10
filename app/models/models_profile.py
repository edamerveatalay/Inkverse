from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from app.models.models_user import User

if TYPE_CHECKING:
    from .models_blog import Blog
    from .models_comment import Comment


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    name: Optional[str] = None
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    bio: Optional[str]
    profile_image: Optional[str]
    website: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="profiles")
