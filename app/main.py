from app.models import User
from fastapi import FastAPI
from app.routers.routers import router
from app.database import engine  # ← burayı ekle
from sqlmodel import SQLModel


app = FastAPI()
app.include_router(router, prefix="/users", tags=["Users"])
#include_router → FastAPI’ye diyoruz ki: “Bu dosyada tanımladığım endpoint’leri de uygulamaya ekle.”
#prefix="/users" → Bütün bu router’daki URL’ler /users/... ile başlasın.
#tags=["users"] → Swagger dokümanında bu endpoint’leri “users” etiketi altında toplasın.

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
