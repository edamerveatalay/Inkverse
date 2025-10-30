from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from app.models.models_blog import Blog
from app.models.models_comment import Comment


class User(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True
    )  # Python’da Optional[X] demek, bu değişkenin X tipinde olabileceğini ama None da olabileceğini ifade eder.
    # default=None → ilk değer yok, veritabanı kendisi atayacak. alan boş olabilir veritabanı değer atayabilir demek
    email: str = Field(index=True, unique=True)
    hashed_password: str
    blogs: List["Blog"] = Relationship(back_populates="author")  # Blog ile ilişki
    comments: List["Comment"] = Relationship(back_populates="author")
