import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from src.order.domain.model.order import Order, OrderItem
from src.order.infrastructure.persistence.postgresql_order_repository import PostgresqlOrderRepository
from src.shared.domain.value_objects import Money

class TestPostgresqlOrderRepository:
    @pytest.fixture
    def order_repository(self, test_session):
        return PostgresqlOrderRepository(test_session)

    @pytest.fixture
    def sample_order(self, mock_user):
        return Order.create(
            customer_name="Test Customer",
            items=[
                OrderItem(
                    product_name="Test Product 1",
                    unit_price=Money(amount=Decimal("10.00")),
                    quantity=2
                ),
                OrderItem(
                    product_name="Test Product 2",
                    unit_price=Money(amount=Decimal("15.00")),
                    quantity=1
                )
            ],
            waiter_id=mock_user.id
        )

    def test_save_order_success(self, test_session):
        # Given
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

        # When
        repository = PostgresqlOrderRepository(test_session)
        saved_order = repository.save(order)

        # Then
        assert saved_order.id is not None
        assert saved_order.customer_name == order.customer_name
        assert len(saved_order.items) == len(order.items)
        assert saved_order.items[0].product_name == order.items[0].product_name
        assert saved_order.items[0].unit_price.amount == order.items[0].unit_price.amount
        assert saved_order.items[0].quantity == order.items[0].quantity

    def test_find_by_id_success(self, order_repository, sample_order):
        # Given
        saved_order = order_repository.save(sample_order)

        # When
        found_order = order_repository.find_by_id(saved_order.id)

        # Then
        assert found_order is not None
        assert found_order.id == saved_order.id
        assert found_order.customer_name == saved_order.customer_name
        assert len(found_order.items) == len(saved_order.items)

    def test_find_by_id_not_found(self, order_repository):
        # When
        found_order = order_repository.find_by_id(999)

        # Then
        assert found_order is None

    def test_find_by_date_range_success(self, order_repository, sample_order):
        # Given
        saved_order = order_repository.save(sample_order)
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=1)

        # When
        orders = order_repository.find_by_date_range(start_date, end_date)

        # Then
        assert len(orders) == 1
        assert orders[0].id == saved_order.id

    def test_get_product_sales_report_success(self, order_repository, sample_order):
        # Given
        order_repository.save(sample_order)
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=1)

        # When
        report = order_repository.get_product_sales_report(start_date, end_date)

        # Then
        assert len(report) == 2
        # Verificar el producto más vendido
        assert report[0]["product_name"] == "Test Product 1"
        assert report[0]["total_quantity"] == 2
        assert report[0]["total_price"] == Decimal("20.00")
        # Verificar el segundo producto
        assert report[1]["product_name"] == "Test Product 2"
        assert report[1]["total_quantity"] == 1
        assert report[1]["total_price"] == Decimal("15.00")
