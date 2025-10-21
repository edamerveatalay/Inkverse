from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# yardımcı fonksiyonlarımızı burada tanımlayacağız

# Şifreleme için context (bcrypt kullanıyoruz)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Şifre hashleme
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Şifre doğrulama (signin sırasında kullanılır)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT Token oluşturma (signin sırasında token döndürmek için)
SECRET_KEY = "super_secret_key"  # Gerçek projede .env'den al
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
