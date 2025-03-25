# services/product_service.py
from sqlalchemy.orm import Session
from core.domain.models import Product
from core.domain.repositories import ProductRepository
from core.domain.services import ProductService
from typing import List, Optional

class ProductServiceImpl(ProductService):
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def get_product(self, db: Session, product_id: int) -> Optional[Product]:
        return self.product_repo.get_by_id(db, product_id)

    def get_all_products(self, db: Session) -> List[Product]:
        return self.product_repo.get_all(db)

    def create_product(self, db: Session, name: str, price: float, image_url: Optional[str] = None) -> Product:
        product = Product(name=name, price=price, image_url=image_url)
        return self.product_repo.create(db, product)