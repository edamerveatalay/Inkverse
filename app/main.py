# app/main.py
from fastapi import FastAPI
from app.database import engine
from sqlmodel import SQLModel
from app.routers.routers import router  # routers klasöründeki ana router

app = FastAPI(title="Inkverse API")

# Tüm router’ları projeye ekliyoruz
app.include_router(router)

#  Veritabanı tabloları uygulama başlarken oluşturulacak
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
