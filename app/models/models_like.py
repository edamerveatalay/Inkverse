from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.models_blog import Blog
    from app.models.models_user import User


class Like(SQLModel, table=True):
    __tablename__ = "likes"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    blog_id: int = Field(foreign_key="blogs.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="likes")
    blog: Optional["Blog"] = Relationship(back_populates="likes")
