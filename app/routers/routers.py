# app/routers/routers.py
from fastapi import APIRouter
from app.routers.auth import get_router, post_router, signin_router
from app.routers.blog import router as blog_router
from app.routers.comments import router as comment_router


router = APIRouter()

# Her endpoint grubunu ayrı çağırıyoruz
router.include_router(get_router)
# include_router : Başka bir dosyada tanımlanmış router’ı (yani endpoint grubunu) bu router’a ekle
router.include_router(post_router)
router.include_router(signin_router)
router.include_router(blog_router)
router.include_router(comment_router)
