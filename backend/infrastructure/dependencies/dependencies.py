from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from decouple import config
from typing import Generator
from core.domain.repositories import ProductRepository, UserRepository
from infrastructure.adapters.repositories.repositories import SQLProductRepository, SQLUserRepository
from core.services.product_service import ProductServiceImpl
from core.services.auth_service import AuthServiceImpl
from core.domain.services import ProductService, AuthService
from fastapi import Depends


DB_USER: str = config('DB_USER')
DB_PASSWORD: str = config('DB_PASSWORD')
DB_HOST: str = config('DB_HOST')
DB_PORT: str = config('DB_PORT')
DB_NAME: str = config('DB_NAME')

DATABASE_URL: str = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # Cambiamos a psycopg

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
                
def get_product_repo(db: Session = Depends(get_db)) -> ProductRepository:
    return SQLProductRepository()

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return SQLUserRepository()

def get_product_service(product_repo: ProductRepository = Depends(get_product_repo)) -> ProductService:
    return ProductServiceImpl(product_repo)

def get_auth_service(user_repo: UserRepository = Depends(get_user_repo)) -> AuthService:
    return AuthServiceImpl(user_repo)