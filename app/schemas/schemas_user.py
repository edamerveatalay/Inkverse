from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    username: str


class UserRead(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
