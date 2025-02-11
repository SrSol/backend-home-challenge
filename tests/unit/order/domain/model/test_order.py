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
        with pytest.raises((ValidationException, ValueError), match="greater than 0"):
            OrderItem(
                product_name="Test Product",
                unit_price=Money(amount=Decimal("0")),
                quantity=1
            )

class TestOrder:
    @pytest.fixture
    def sample_items(self):
        return [
            OrderItem(
                product_name="Test Product",
                unit_price=Money(amount=Decimal("10.00")),
                quantity=2
            ),
            OrderItem(
                product_name="Test Product",  # Mismo producto
                unit_price=Money(amount=Decimal("10.00")),
                quantity=3
            ),
            OrderItem(
                product_name="Other Product",
                unit_price=Money(amount=Decimal("15.00")),
                quantity=1
            )
        ]

    def test_create_order_combines_duplicate_items(self):
        # Given
        items = [
            OrderItem(
                product_name="Test Product",
                unit_price=Money(amount=Decimal("10.00")),
                quantity=2
            ),
            OrderItem(
                product_name="Test Product",  # Mismo producto
                unit_price=Money(amount=Decimal("10.00")),
                quantity=3
            ),
            OrderItem(
                product_name="Other Product",
                unit_price=Money(amount=Decimal("15.00")),
                quantity=1
            )
        ]

        # When
        order = Order.create(
            customer_name="Test Customer",
            items=items,
            waiter_id=1
        )

        # Then
        assert len(order.items) == 2  # Debería haber combinado los items duplicados

        # Verificar el item combinado
        test_product_item = next(
            item for item in order.items 
            if item.product_name == "Test Product"
        )
        assert test_product_item.quantity == 5  # 2 + 3
        assert test_product_item.unit_price.amount == Decimal("10.00")

        # Verificar el otro item
        other_product_item = next(
            item for item in order.items 
            if item.product_name == "Other Product"
        )
        assert other_product_item.quantity == 1
        assert other_product_item.unit_price.amount == Decimal("15.00")

    def test_order_total_amount_with_combined_items(self, sample_items):
        # When
        order = Order.create(
            customer_name="Test Customer",
            items=sample_items,
            waiter_id=1
        )

        # Then
        # Total = (10.00 * 5) + (15.00 * 1) = 50.00 + 15.00 = 65.00
        assert order.total_amount.amount == Decimal("65.00")

    def test_order_total_price_with_combined_items(self):
        # Given
        items = [
            OrderItem(
                product_name="Test Product",
                unit_price=Money(amount=Decimal("10.00")),
                quantity=2
            ),
            OrderItem(
                product_name="Test Product",
                unit_price=Money(amount=Decimal("10.00")),
                quantity=3
            )
        ]

        # When
        order = Order.create(
            customer_name="Test Customer",
            items=items,
            waiter_id=1
        )

        # Then
        assert len(order.items) == 1
        assert order.total_price.amount == Decimal("50.00")
