import pytest
from decimal import Decimal
from src.product.domain.model.product import Product
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects import Money

class TestProductModel:
    def test_create_product_success(self):
        # When
        product = Product.create(
            name="Test Product",
            price=Decimal("10.00")
        )

        # Then
        assert product.name == "Test Product"
        assert product.current_price.amount == Decimal("10.00")
        assert product.id is None

    @pytest.mark.parametrize("invalid_name", ["", " ", "a"])
    def test_create_product_with_invalid_name_fails(self, invalid_name):
        # When/Then
        with pytest.raises(ValidationException, match="Product name must be at least 2 characters long"):
            Product.create(
                name=invalid_name,
                price=Decimal("10.00")
            )

    @pytest.mark.parametrize("invalid_price", [
        Decimal("0.00"),
        Decimal("-1.00")
    ])
    def test_create_product_with_invalid_price_fails(self, invalid_price):
        # When/Then
        with pytest.raises(ValidationException, match="Price must be greater than 0"):
            Product.create(
                name="Test Product",
                price=invalid_price
            ) 