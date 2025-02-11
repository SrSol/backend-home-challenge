from decimal import Decimal
from typing import List, Optional
from src.product.domain.model.product import Product
from src.product.domain.repository.product_repository import ProductRepository
from src.shared.domain.exceptions import ValidationException

class ProductService:
    """Domain service for product-related business operations"""

    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository

    def create_or_update_product(self, name: str, price: Decimal) -> Product:
        """Creates a new product or updates its price if it already exists"""
        existing_product = self._product_repository.find_by_name(name)
        
        if existing_product:
            if existing_product.current_price.amount != price:
                return self._product_repository.update_price(
                    product_id=existing_product.id,
                    new_price=price
                )
            return existing_product
        
        product = Product.create(name=name, price=price)
        return self._product_repository.save(product)

    def get_product_by_name(self, name: str) -> Optional[Product]:
        """Gets a product by name"""
        return self._product_repository.find_by_name(name)

    def get_all_products(self) -> List[Product]:
        """Gets all products"""
        return self._product_repository.find_all() 