# core/domain/services.py
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from core.domain.models import Product, User
from typing import List, Optional

class ProductService(ABC):
    @abstractmethod
    def get_product(self, db: Session, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all_products(self, db: Session) -> List[Product]:
        pass

    @abstractmethod
    def create_product(self, db: Session, name: str, price: float, image_url: Optional[str] = None) -> Product:
        pass

class AuthService(ABC):
    @abstractmethod
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        pass

    @abstractmethod
    def create_access_token(self, data: dict[str, str]) -> str:
        pass