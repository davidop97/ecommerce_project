# controllers/product_controller.py
from sqlalchemy.orm import Session
from core.domain.services import ProductService
from infrastructure.adapters.contracts.contracts import ProductResponse
from fastapi import HTTPException
from typing import List

class ProductController:
    def __init__(self, product_service: ProductService):
        self.product_service = product_service

    def get_product(self, db: Session, product_id: int) -> ProductResponse:
        product = self.product_service.get_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductResponse.model_validate(product)

    def get_all_products(self, db: Session) -> List[ProductResponse]:
        products = self.product_service.get_all_products(db)
        return [ProductResponse.model_validate(p) for p in products]

    def create_product(self, db: Session, name: str, price: float, image_url: str | None) -> ProductResponse:
        product = self.product_service.create_product(db, name, price, image_url)
        return ProductResponse.model_validate(product)