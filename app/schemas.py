from pydantic import BaseModel 

class UserCreate (BaseModel):
    email: str
    password: str 


class UserRead (BaseModel) : #kullanıcıya gösterilecek kısım hashed_password yok çünkü güvenlik için gizli 
    id : int
    email : str

    class Config:  # <-- Config UserRead modelinin içinde olmalı
        from_attributes = True
