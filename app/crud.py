from passlib import CryptContext 

async def get_user_by_email (session: AsyncSession, email: str ) :
 result = await session.execute(select(User).where(User.email == email))
#session veritabanı bağlantısı sağlar 
#execute User sql sorgusunun çalıştırılmasını sağlar 
#user.email == User tablosundan email sütunu bu kullanıcıya eşit olan satırı getir. istediğim email veritabanında buna eşit olduğunda demek
 return result.scalar_one_or_none()
#Eğer tam bir kullanıcı nesnesi varsa onu döndürür. Eğer hiç sonuç yoksa, None döner.

pwd_context = CryptContext(schemes = ["bcrypt"])#pwd_context sabit bir araçtır; uygulama başlarken bir kez tanımlanır, sonra her yerde kullanılır.

async def create_userse (session: AsyncSession, user_data: UserCreate ): #usercreate sınıfından verileri aldık (email, password)
 # artık verilere Burada user_data.email ve user_data.password şeklinde erişeceksin.
 existing_user = await get_user_by_email(session, user_data.email)
#existing_user = “veritabanında zaten kayıtlı olan kullanıcı” anlamına geliyor.
#yani biz existing_user diye bi değişken tanımlayıp get_user_by_email fonksiyonunun çağrılmış halini de buna atadık

hashed_password = pwd_context.hash(user_data.password)
new_user = User(email = user_data.email, hashed_password = hashed_password)
session.add(new_user)
await session.commit()
