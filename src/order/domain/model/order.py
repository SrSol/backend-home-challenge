from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects import Money
from decimal import Decimal

@dataclass(frozen=True)
class OrderItem:
    """Value object representing an item in an order"""
    product_name: str
    unit_price: Money
    quantity: int
    id: Optional[int] = None

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValidationException("Quantity must be greater than 0")
        if self.unit_price.amount <= 0:
            raise ValidationException("Unit price must be greater than 0")

    @property
    def total_price(self) -> Money:
        return self.unit_price * self.quantity

@dataclass(frozen=True)
class Order:
    """Order aggregate root entity"""
    customer_name: str
    items: List[OrderItem]
    waiter_id: int
    created_at: datetime
    id: Optional[int] = None

    def __post_init__(self):
        if not self.customer_name or len(self.customer_name.strip()) < 2:
            raise ValidationException("Customer name must be at least 2 characters long")
        if not self.items:
            raise ValidationException("Order must have at least one item")
        if self.waiter_id < 1:
            raise ValidationException("Invalid waiter id")

    @property
    def total_price(self) -> Money:
        # Crear un Money con Decimal('0.01') como valor inicial
        zero_money = Money(amount=Decimal('0.01'))
        if not self.items:
            return zero_money
        
        # Sumar los precios totales de cada item
        total = sum((item.total_price.amount for item in self.items), Decimal('0'))
        return Money(amount=total)

    @staticmethod
    def create(customer_name: str, items: List[OrderItem], waiter_id: int) -> 'Order':
        """Factory method to create a new order"""
        return Order(
            customer_name=customer_name,
            items=items,
            waiter_id=waiter_id,
            created_at=datetime.utcnow()
        ) 