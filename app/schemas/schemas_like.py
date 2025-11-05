from pydantic import BaseModel
from app.schemas.schemas_user import UserRead


class LikeCreate(BaseModel):

    blog_id: int


class LikeRead(BaseModel):
    id: int
    user_id: int
    blog_id: int

    class Config:
        from_attributes = True


class LikeOut(BaseModel):  # Beğenen kullanıcıları göstermek için
    id: int
    user_id: int
    blog_id: int
    user: UserRead

    class Config:
        from_attributes = True


class LikeDelete(BaseModel):
    user_id: int
    blog_id: int
