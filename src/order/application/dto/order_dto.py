from pydantic import BaseModel, Field, field_validator
from typing import List
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
        """Convierte el DTO a una entidad de dominio"""
        from src.order.domain.model.order import Order, OrderItem
        from src.shared.domain.value_objects import Money
        
        items = [
            OrderItem(
                product_name=item.product_name,
                unit_price=Money(amount=item.unit_price),
                quantity=item.quantity
            )
            for item in self.items
        ]
        
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

class ProductSalesReportDTO(BaseModel):
    """DTO for product sales report"""
    product_name: str
    total_quantity: int
    total_price: Decimal 