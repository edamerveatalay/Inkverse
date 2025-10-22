from pydantic import BaseModel
from datetime import datetime


class BlogCreate(BaseModel):
    title: str
    content: str


class BlogRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True
        # gelen verinin direkt python objesine çevrilmesini sağlar


class BlogUpdate(BaseModel):  # blog güncellerken değiştirilecek alanlar
    title: str
    content: str
