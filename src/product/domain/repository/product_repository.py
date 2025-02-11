from abc import ABC, abstractmethod
from typing import Optional, List
from decimal import Decimal
from src.product.domain.model.product import Product

class ProductRepository(ABC):
    """Repository interface for Product aggregate"""

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Saves a product and returns the saved entity"""
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Product]:
        """Finds a product by name"""
        pass

    @abstractmethod
    def find_all(self) -> List[Product]:
        """Returns all products"""
        pass

    @abstractmethod
    def update_price(self, product_id: int, new_price: Decimal) -> Product:
        """Updates product price"""
        pass 