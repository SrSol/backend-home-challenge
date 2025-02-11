from typing import List, Optional
from datetime import datetime
from src.order.domain.model.order import Order, OrderItem
from src.order.domain.repository.order_repository import OrderRepository
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects import Money

class OrderService:
    """Domain service for order-related business operations"""

    def __init__(self, order_repository: OrderRepository):
        self._order_repository = order_repository

    def create_order(
        self, 
        customer_name: str, 
        items: List[dict],
        waiter_id: int
    ) -> Order:
        """Creates a new order"""
        order_items = [
            OrderItem(
                product_name=item["product_name"],
                unit_price=Money(amount=item["unit_price"]),
                quantity=item["quantity"]
            )
            for item in items
        ]
        
        order = Order.create(
            customer_name=customer_name,
            items=order_items,
            waiter_id=waiter_id
        )
        
        return self._order_repository.save(order)

    def get_product_sales_report(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[dict]:
        """Gets product sales report within a date range"""
        return self._order_repository.get_product_sales_report(
            start_date=start_date,
            end_date=end_date
        ) 