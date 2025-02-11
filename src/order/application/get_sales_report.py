from typing import List
from src.order.domain.service.order_service import OrderService
from src.order.application.dto.order_dto import ProductSalesReportDTO
from src.shared.domain.value_objects import DateTimeRange

class GetSalesReportQuery:
    """Application service for getting sales report"""

    def __init__(self, order_service: OrderService):
        self._order_service = order_service

    def execute(self, date_range: DateTimeRange) -> List[ProductSalesReportDTO]:
        """
        Gets sales report for date range

        Args:
            date_range: Start and end dates for report

        Returns:
            List of products with sales data, ordered by quantity
        """
        report = self._order_service.get_product_sales_report(
            start_date=date_range.start_date,
            end_date=date_range.end_date
        )

        return [ProductSalesReportDTO(**item) for item in report]
