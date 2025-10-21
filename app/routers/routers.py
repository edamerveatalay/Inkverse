# app/routers/routers.py
from fastapi import APIRouter
from app.auth import get_router, post_router, signin_router

router = APIRouter()

# Her endpoint grubunu ayrı çağırıyoruz
router.include_router(get_router)
# include_router : Başka bir dosyada tanımlanmış router’ı (yani endpoint grubunu) bu router’a ekle
router.include_router(post_router)
router.include_router(signin_router)  # ← burayı ekledik
