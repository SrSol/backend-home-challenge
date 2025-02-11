from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects import Money
from datetime import datetime

@dataclass(frozen=True)
class Product:
    """Product aggregate root entity"""
    name: str
    current_price: Money
    created_at: datetime
    updated_at: datetime
    id: Optional[int] = None

    def __post_init__(self):
        if not self.name or len(self.name.strip()) < 2:
            raise ValidationException("Product name must be at least 2 characters long")
        if self.current_price.amount <= 0:
            raise ValidationException("Price must be greater than 0")

    @staticmethod
    def create(name: str, price: Decimal) -> 'Product':
        """Factory method to create a new product"""
        now = datetime.utcnow()
        return Product(
            name=name,
            current_price=Money(amount=price),
            created_at=now,
            updated_at=now
        ) 