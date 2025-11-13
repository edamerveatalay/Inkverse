# app/main.py
from fastapi import FastAPI
from app.database import engine
from sqlmodel import SQLModel
from app.routers.routers import router  # routers klasöründeki ana router
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")


app = FastAPI(title="Inkverse API")

# Tüm router’ları projeye ekliyoruz
app.include_router(router)


#  Veritabanı tabloları uygulama başlarken oluşturulacak
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@app.get("/health")
def health_check():
    return {"status": "OK"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Inkverse API",
        version="1.0.0",
        description="Inkverse Blog API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Tüm endpointlere security ekle
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [
                {"OAuth2PasswordBearer": []}
            ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
