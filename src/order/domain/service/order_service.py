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

    def create_order(self, order: Order) -> Order:
        """Creates a new order"""
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