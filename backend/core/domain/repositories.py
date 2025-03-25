# core/domain/repositories.py
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from core.domain.models import Product, User
from typing import List, Optional

class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self, db: Session) -> List[Product]:
        pass

    @abstractmethod
    def create(self, db: Session, product: Product) -> Product:
        pass

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, db: Session, user: User) -> User:
        pass