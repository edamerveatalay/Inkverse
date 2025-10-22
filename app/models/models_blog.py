from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime  # ← bunu eklemelisin
from app.models.models_user import User


class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str  # yazının içerik kısmı
    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )  # şu anki zamanı çeker
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    author: Optional[User] = Relationship(back_populates="blogs")


User.blogs = Relationship(back_populates="author")
# her kullanıcı (User) objesinin sahip olduğu tüm bloglara (Blog) user.blogs ile Python üzerinden erişebilmesini sağlar ve bu ilişki Blog modelindeki author alanı ile çift yönlü bağlanır.
# Yani biz kullanıcıyla blogu bağladık hangi kullanıcı nereye yazdı bunun takibini sağlıyoruz
