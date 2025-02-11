import pytest
from datetime import datetime
from decimal import Decimal
from src.order.domain.model.order import Order, OrderItem
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects import Money

class TestOrderModel:
    @pytest.fixture
    def valid_order_item(self):
        return OrderItem(
            product_name="Test Product",
            unit_price=Money(amount=Decimal("10.00")),
            quantity=2
        )

    def test_create_order_success(self, valid_order_item):
        # When
        order = Order.create(
            customer_name="Test Customer",
            items=[valid_order_item],
            waiter_id=1
        )

        # Then
        assert order.customer_name == "Test Customer"
        assert len(order.items) == 1
        assert order.waiter_id == 1
        assert order.created_at is not None
        assert order.total_price.amount == Decimal("20.00")

    @pytest.mark.parametrize("invalid_name", ["", " ", "a"])
    def test_create_order_with_invalid_customer_name_fails(self, invalid_name, valid_order_item):
        # When/Then
        with pytest.raises(ValidationException, match="Customer name must be at least 2 characters long"):
            Order.create(
                customer_name=invalid_name,
                items=[valid_order_item],
                waiter_id=1
            )

    def test_create_order_with_empty_items_fails(self):
        # When/Then
        with pytest.raises(ValidationException, match="Order must have at least one item"):
            Order.create(
                customer_name="Test Customer",
                items=[],
                waiter_id=1
            )

    def test_create_order_with_invalid_waiter_id_fails(self, valid_order_item):
        # When/Then
        with pytest.raises(ValidationException, match="Invalid waiter id"):
            Order.create(
                customer_name="Test Customer",
                items=[valid_order_item],
                waiter_id=0
            )

class TestOrderItemModel:
    def test_create_order_item_success(self):
        # When
        item = OrderItem(
            product_name="Test Product",
            unit_price=Money(amount=Decimal("10.00")),
            quantity=2
        )

        # Then
        assert item.product_name == "Test Product"
        assert item.unit_price.amount == Decimal("10.00")
        assert item.quantity == 2
        assert item.total_price.amount == Decimal("20.00")

    @pytest.mark.parametrize("invalid_product_name", ["", " ", "a"])
    def test_create_order_item_with_invalid_product_name_fails(self, invalid_product_name):
        # When/Then
        with pytest.raises(ValidationException, match="Product name must be at least 2 characters long"):
            OrderItem(
                product_name=invalid_product_name,
                unit_price=Money(amount=Decimal("10.00")),
                quantity=1
            )

    def test_create_order_item_with_invalid_quantity_fails(self):
        # When/Then
        with pytest.raises(ValidationException, match="Quantity must be greater than 0"):
            OrderItem(
                product_name="Test Product",
                unit_price=Money(amount=Decimal("10.00")),
                quantity=0
            )

    def test_create_order_item_with_invalid_price_fails(self):
        # When/Then
        with pytest.raises(ValidationException, match="Unit price must be greater than 0"):
            OrderItem(
                product_name="Test Product",
                unit_price=Money(amount=Decimal("0")),
                quantity=1
            ) 