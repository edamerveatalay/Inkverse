from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas_user import UserCreate, UserRead  # Şema modellerin
from app.models.models_user import User
from sqlalchemy import select


async def get_user_by_email(
    session: AsyncSession, email: str
):  # read işlemi okuma işlemi yapıyor.
    result = await session.execute(select(User).where(User.email == email))
    # session veritabanı bağlantısı sağlar
    # execute User sql sorgusunun çalıştırılmasını sağlar
    # user.email == User tablosundan email sütunu bu kullanıcıya eşit olan satırı getir. istediğim email veritabanında buna eşit olduğunda demek
    return result.scalar_one_or_none()


# Eğer tam bir kullanıcı nesnesi varsa onu döndürür. Eğer hiç sonuç yoksa, None döner.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# pwd_context sabit bir araçtır; uygulama başlarken bir kez tanımlanır, sonra her yerde kullanılır.


async def create_user(session: AsyncSession, user_data: UserCreate):
    existing_user = await get_user_by_email(session, user_data.email)
    if existing_user:
        raise ValueError("User already exists")

    hashed_password = pwd_context.hash(user_data.password.encode("utf-8"))
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        username=user_data.username,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_all_users(session: AsyncSession):
    result = await session.execute(
        select(User)
    )  # Bu komut, veritabanına gerçek sorguyu gönderir.
    # select(User) tek başına sadece bir hazırlanmış sorgudur. Ama bu sorgunun çalışması için bir bağlantıya (session’a) ihtiyacın vardır.
    # işte session.execute() bunu yapar
    # yani Bu sorguyu veritabanında çalıştır. demek
    users = (
        result.scalars().all()
    )  # .scalars() bu satırları sadece model nesnelerine çevirir.
    return users
