import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock
from src.order.domain.service.order_service import OrderService
from src.order.domain.model.order import Order, OrderItem
from src.shared.domain.value_objects import Money

class TestOrderService:
    @pytest.fixture
    def order_repository(self):
        return Mock()

    @pytest.fixture
    def order_service(self, order_repository):
        return OrderService(order_repository)

    @pytest.fixture
    def sample_items(self):
        return [
            {
                "product_name": "Test Product 1",
                "unit_price": Decimal("10.00"),
                "quantity": 2
            },
            {
                "product_name": "Test Product 2",
                "unit_price": Decimal("15.00"),
                "quantity": 1
            }
        ]

    def test_create_order_success(self, order_repository):
        # Given
        service = OrderService(order_repository)
        order = Order.create(
            customer_name="Test Customer",
            items=[
                OrderItem(
                    product_name="Test Product",
                    unit_price=Money(amount=Decimal("10.00")),
                    quantity=2
                )
            ],
            waiter_id=1
        )
        order_repository.save.return_value = order
        
        # When
        result = service.create_order(order)
        
        # Then
        assert isinstance(result, Order)
        order_repository.save.assert_called_once_with(order)

    def test_get_product_sales_report_success(self, order_service, order_repository):
        # Given
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        
        expected_report = [
            {
                "product_name": "Test Product 1",
                "total_quantity": 5,
                "total_price": Decimal("50.00")
            }
        ]
        order_repository.get_product_sales_report.return_value = expected_report

        # When
        result = order_service.get_product_sales_report(
            start_date=start_date,
            end_date=end_date
        )

        # Then
        assert result == expected_report
        order_repository.get_product_sales_report.assert_called_once_with(
            start_date=start_date,
            end_date=end_date
        ) 