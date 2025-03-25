from sqlalchemy.orm import Session
from core.domain.models import Product, User
from core.domain.repositories import ProductRepository, UserRepository
from typing import List, Optional

class SQLProductRepository(ProductRepository):
    def get_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    def get_all(self, db: Session) -> List[Product]:
        return db.query(Product).all()

    def create(self, db: Session, product: Product) -> Product:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

class SQLUserRepository(UserRepository):
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user