from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.dependencies.dependencies import get_db, get_product_service
from core.domain.services import ProductService
from infrastructure.adapters.contracts.contracts import ProductResponse
from core.domain.models import User
from infrastructure.routes.auth_routes import get_current_user
from infrastructure.controllers.product_controller import ProductController
from infrastructure.routes.auth_routes import get_current_user
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

def get_product_controller(product_service: ProductService = Depends(get_product_service)) -> ProductController:
    return ProductController(product_service)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    controller: ProductController = Depends(get_product_controller),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ProductResponse:
    return controller.get_product(db, product_id)

@router.get("/", response_model=List[ProductResponse])
async def get_all_products(
    controller: ProductController = Depends(get_product_controller),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Añadimos autenticación
) -> List[ProductResponse]:
    return controller.get_all_products(db)

@router.post("/", response_model=ProductResponse)
async def create_product(
    name: str,
    price: float,
    image_url: str | None = None,
    controller: ProductController = Depends(get_product_controller),
    db: Session = Depends(get_db)
) -> ProductResponse:
    return controller.create_product(db, name, price, image_url)