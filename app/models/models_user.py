from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .models_blog import Blog
    from .models_comment import Comment
    from .models_profile import Profile
    from .models_like import Like


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)

    blogs: List["Blog"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    comments: List["Comment"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    profiles: Optional["Profile"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    likes: List["Like"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )


from app.models.models_profile import Profile
