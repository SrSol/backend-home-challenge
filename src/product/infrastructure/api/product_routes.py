from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.shared.infrastructure.persistence.database import get_db
from src.shared.infrastructure.api.dependencies import get_current_user
from src.product.application.dto.product_dto import ProductResponseDTO
from src.product.application.get_products import GetProductsQuery
from src.product.domain.service.product_service import ProductService
from src.product.infrastructure.persistence.postgresql_product_repository import PostgresqlProductRepository

router = APIRouter(prefix="/products", tags=["products"])

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repository = PostgresqlProductRepository(db)
    return ProductService(repository)

@router.get("/", response_model=List[ProductResponseDTO])
def get_products(
    current_user: str = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
):
    """Gets all products"""
    query = GetProductsQuery(product_service)
    return query.execute() 