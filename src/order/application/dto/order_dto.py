from pydantic import BaseModel, Field, field_validator
from typing import List
from src.order.domain.model.order import Order
from datetime import datetime
from decimal import Decimal

class OrderItemDTO(BaseModel):
    """DTO for order item creation"""
    product_name: str = Field(..., min_length=2)
    unit_price: Decimal
    quantity: int = Field(..., gt=0)

    @field_validator('unit_price', mode='before')
    def validate_unit_price(cls, v):
        if isinstance(v, str):
            try:
                v = Decimal(v)
            except:
                raise ValueError("Invalid unit price format")
        if v <= 0:
            raise ValueError("Unit price must be greater than 0")
        return v

    model_config = {
        "json_encoders": {
            Decimal: str
        }
    }

class CreateOrderDTO(BaseModel):
    """DTO for order creation"""
    customer_name: str = Field(..., min_length=2)
    items: List[OrderItemDTO]

    @field_validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError("Order must have at least one item")
        return v

    def to_domain(self, waiter_id: int) -> 'Order':
        """Converts DTO to domain entity"""
        from src.order.domain.model.order import Order, OrderItem
        from src.shared.domain.value_objects import Money

        items = []
        for item in self.items:
            # Ensure price is Decimal
            try:
                unit_price = Money(amount=item.unit_price)
            except Exception as e:
                raise ValueError(f"Invalid unit price: {item.unit_price} ({type(item.unit_price)})")

            items.append(
                OrderItem(
                    product_name=item.product_name,
                    unit_price=unit_price,
                    quantity=item.quantity
                )
            )

        return Order.create(
            customer_name=self.customer_name,
            items=items,
            waiter_id=waiter_id
        )

class OrderResponseDTO(BaseModel):
    """DTO for order responses"""
    id: int
    customer_name: str
    items: List[OrderItemDTO]
    total_price: Decimal
    waiter_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            Decimal: str
        }
    }

    @classmethod
    def from_entity(cls, order: 'Order') -> 'OrderResponseDTO':
        """Converts Order entity to DTO"""
        return cls(
            id=order.id,
            customer_name=order.customer_name,
            items=[
                OrderItemDTO(
                    product_name=item.product_name,
                    unit_price=item.unit_price.amount,
                    quantity=item.quantity
                )
                for item in order.items
            ],
            total_price=order.total_price.amount,
            waiter_id=order.waiter_id,
            created_at=order.created_at
        )


class ProductSalesReportDTO(BaseModel):
    """DTO for product sales report response"""
    product_name: str
    total_quantity: int
    total_price: Decimal

    class Config:
        from_attributes = True

class DateRangeDTO(BaseModel):
    """DTO for date range filter"""
    start_date: datetime
    end_date: datetime
