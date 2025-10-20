from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os 
from dotenv import load_dotenv
#os → Python’un standart kütüphanesi, işletim sistemi ile ilgili işlemler yapmamızı sağlar.
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from fastapi import Depends



load_dotenv() 
#Bu bir hazır fonksiyon.
#Amacı: .env dosyasındaki tüm satırları okuyup, onları sistemin ortam değişkenleri (os.environ) içine eklemek.
DATABASE_URL = os.environ.get("DATABASE_URL")
#.env içindeki veriyi DATABASE_URL değişkenine aktardık.
#DATABASE_URL adlı ortam değişkenini oku, Eğer böyle bir değişken yoksa None döndür. demek bu satır 
#Biz veritabanına bağlanırken URL’i bir değişkende tutmak istiyoruz.
#Böylece sonraki adımlarda (engine ve sessionmaker oluştururken) direkt DATABASE_URL değişkenini kullanabiliriz.

#os.environ → sistemdeki tüm ortam değişkenlerini tutan bir sözlük (dict) gibidir.

engine = create_async_engine(DATABASE_URL)
#veritabanı bağlantısını artık engine yönetiyor 

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#async_session_maker:  SQLAlchemy’nin async session oluşturma fabrikasıdır.
#Her çağrıldığında yeni bir veritabanı oturumu (session) oluşturur.
#engine kullanarak: Session maker’a veriyoruz çünkü hangi veritabanı bağlantısını kullanacağını bilmesi gerekiyor.
#class_=AsyncSession:  SQLAlchemy’de session oluştururken hangi sınıfı kullanacağını belirtiyoruz.
#Normalde SQLAlchemy’de commit işlemi yapınca session’daki objeler “expire” olur, yani veriler tekrar veritabanından çekilir. False yaparsak commit sonrası session’daki objeler hâlâ kullanılabilir, böylece verileri tekrar sorgulamak zorunda kalmayız.

#Session, veritabanıyla konuşmamızı sağlayan geçici bağlantı ve işlem konteyneridir; içinde sorgular çalışır, değişiklikler takip edilir ve commit ile kalıcı hale gelir.


async def get_session() :
    #Her HTTP isteğinde FastAPI’ye yeni bir veritabanı oturumu (session) sağlar get_session fonksiyonu 
    async with async_session_maker() as session:
        #Bu satırda async_session_maker() çağırarak yeni bir veritabanı oturumu oluşturuyorsun.
        #async_sessionmaker → SQLAlchemy’nin bize sunduğu hazır bir sınıf
        yield session
        #İşte bu session’ı endpoint içinde kullan.
        #Session = Veritabanına sorgu göndermemizi, veri eklememizi, güncellememizi veya silmemizi sağlayan bağlantı yöneticisidir.