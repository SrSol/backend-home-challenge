from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from src.order.domain.model.order import Order

class OrderRepository(ABC):
    """Repository interface for Order aggregate"""

    @abstractmethod
    def save(self, order: Order) -> Order:
        """Saves an order and returns the saved entity"""
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Order]:
        """Finds an order by id"""
        pass

    @abstractmethod
    def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Order]:
        """Finds orders within a date range"""
        pass

    @abstractmethod
    def get_product_sales_report(self, start_date: datetime, end_date: datetime) -> List[dict]:
        """Gets product sales report within a date range"""
        pass 