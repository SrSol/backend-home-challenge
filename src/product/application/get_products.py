from typing import List
from src.product.domain.service.product_service import ProductService
from src.product.application.dto.product_dto import ProductResponseDTO

class GetProductsQuery:
    """Application service for getting products"""

    def __init__(self, product_service: ProductService):
        self._product_service = product_service

    def execute(self) -> List[ProductResponseDTO]:
        """Gets all products"""
        products = self._product_service.get_all_products()
        
        return [
            ProductResponseDTO(
                id=product.id,
                name=product.name,
                current_price=product.current_price.amount,
                created_at=product.created_at,
                updated_at=product.updated_at
            )
            for product in products
        ] 