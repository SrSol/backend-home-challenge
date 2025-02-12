from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timezone
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects import Money

@dataclass(frozen=True)
class OrderItem:
    """Value object representing an item in an order"""
    product_name: str
    unit_price: Money
    quantity: int
    id: Optional[int] = None

    def __post_init__(self):
        """Validates the order item after initialization"""
        if not self.product_name or len(self.product_name.strip()) < 2:
            raise ValidationException("Product name must be at least 2 characters long")
        if self.quantity <= 0:
            raise ValidationException("Quantity must be greater than 0")
        if self.unit_price.amount <= 0:
            raise ValidationException("Unit price must be greater than 0")

    @property
    def total_price(self) -> Money:
        return self.unit_price * self.quantity

@dataclass
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
        # Combine items with the same product name after validation
        self.items = self._combine_duplicate_items(self.items)

    def _combine_duplicate_items(self, items: List[OrderItem]) -> List[OrderItem]:
        """
        Combines items with the same product name by summing their quantities

        Args:
            items: List of order items to combine

        Returns:
            List of combined order items
        """
        combined_items = {}

        for item in items:
            if item.product_name in combined_items:
                # If product exists, create new item with summed quantity
                existing = combined_items[item.product_name]
                combined_items[item.product_name] = OrderItem(
                    id=existing.id,
                    product_name=existing.product_name,
                    unit_price=existing.unit_price,
                    quantity=existing.quantity + item.quantity
                )
            else:
                # If new product, add to dictionary
                combined_items[item.product_name] = item

        return list(combined_items.values())

    @property
    def total_price(self) -> Money:
        return Money(amount=sum(item.total_price.amount for item in self.items))

    @staticmethod
    def create(customer_name: str, items: List[OrderItem], waiter_id: int) -> 'Order':
        """Factory method to create a new order"""
        return Order(
            customer_name=customer_name,
            items=items,
            waiter_id=waiter_id,
            created_at=datetime.now(timezone.utc)
        )

    @property
    def total_amount(self) -> Money:
        return Money(
            amount=sum(item.total_price.amount for item in self.items)
        )
