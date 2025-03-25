from sqlalchemy.orm import Session
from core.domain.models import User
from core.domain.repositories import UserRepository
from core.domain.services import AuthService
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone 
from decouple import config
from typing import Optional, Dict
from jose import jwt

SECRET_KEY: str = config('SECRET_KEY')
ALGORITHM: str = config('ALGORITHM', default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=30)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthServiceImpl(AuthService):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password) is True

    def get_password_hash(self, password: str) -> str:
        return str(pwd_context.hash(password))

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_email(db, email)
        if not user or not self.verify_password(password, user.password):
            return None
        return user

    def create_access_token(self, data: Dict[str, str]) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": str(int(expire.timestamp()))})
        print("SECRET_KEY en generación:", SECRET_KEY)  # Añadimos aquí
        print("Token payload:", to_encode)  # Para ver el payload antes de codificar
        return str(jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM))