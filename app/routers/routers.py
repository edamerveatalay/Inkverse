from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session   # veritabanı bağlantısı
from app.schemas import UserCreate, UserRead  # şemalar (giriş/çıkış modelleri)
from app.crud  import create_user, get_all_users  # CRUD fonksiyonları


router = APIRouter( tags=["Users"])
#router birden fazla endpointi tutuyor 
## tags=["Users"]: Swagger dokümantasyonunda bu endpointleri “Users” başlığı altında gruplayarak daha düzenli gösterir


@router.get ("/", response_model=list[UserRead])#get isteklerini yakalayan endpoint 
async def get_users(session: AsyncSession = Depends(get_session)):
    #response_model=list[UserRead]: kullanıcıya dönecek veri tipi (şema). Kullanıcıya liste şeklinde dönecek
    #response model da kullanıcıya veri döndürmeye yarar 
    #session, veritabanıyla konuşmamızı sağlayan nesnedir.
    users = await get_all_users (session)
    return users 

@router.post("/", response_model = list[UserRead],status_code=status.HTTP_201_CREATED )
async def create_new_users(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    #user_data → istek body’sinden gelen JSON veriyi alır.
        #session → veritabanı bağlantısını sağlar (Depends(get_session) sayesinde).
    user = await create_user(session, user_data)
    return [UserRead.from_orm(user)]
#user = await create_user(session, user_data) yeni kullanıcıyı ekleyen kısım, oluşturulan kullanıcıyı veritabanı bağlantısı oluşturarak (session ile) ve user_data ile kullanıcı bilgilerini alarak user değişkenine yani yeni bir kullanıcıya atıyor.


#@router.post("/"): POST isteği geldiğinde /users/ yolunu dinler.

#user_data: kullanıcıdan gelen body verisi (email, password).
#create_user(): yeni kullanıcıyı veritabanına ekler.
#status_code=201: HTTP’de “Created” anlamına gelir.