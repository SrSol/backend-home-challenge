import pytest
from decimal import Decimal
from datetime import datetime
from unittest.mock import Mock
from src.product.domain.service.product_service import ProductService
from src.product.domain.model.product import Product
from src.shared.domain.value_objects import Money

class TestProductService:
    @pytest.fixture
    def product_repository(self):
        return Mock()

    @pytest.fixture
    def product_service(self, product_repository):
        return ProductService(product_repository)

    @pytest.fixture
    def sample_product(self):
        now = datetime.utcnow()
        return Product(
            id=1,
            name="Test Product",
            current_price=Money(amount=Decimal("10.00")),
            created_at=now,
            updated_at=now
        )

    def test_create_new_product_success(self, product_service, product_repository, sample_product):
        # Given
        product_repository.find_by_name.return_value = None
        product_repository.save.return_value = sample_product

        # When
        result = product_service.create_or_update_product(
            name="Test Product",
            price=Decimal("10.00")
        )

        # Then
        assert result == sample_product
        product_repository.save.assert_called_once()

    def test_update_existing_product_price_success(self, product_service, product_repository, sample_product):
        # Given
        product_repository.find_by_name.return_value = sample_product
        now = datetime.utcnow()
        updated_product = Product(
            id=1,
            name="Test Product",
            current_price=Money(amount=Decimal("15.00")),
            created_at=sample_product.created_at,  # Mantener created_at original
            updated_at=now  # Nueva fecha de actualización
        )
        product_repository.update_price.return_value = updated_product

        # When
        result = product_service.create_or_update_product(
            name="Test Product",
            price=Decimal("15.00")
        )

        # Then
        assert result == updated_product
        product_repository.update_price.assert_called_once_with(
            product_id=1,
            new_price=Decimal("15.00")
        )

    def test_get_existing_product_success(self, product_service, product_repository, sample_product):
        # Given
        product_repository.find_by_name.return_value = sample_product

        # When
        result = product_service.get_product_by_name("Test Product")

        # Then
        assert result == sample_product
        product_repository.find_by_name.assert_called_once_with("Test Product")

    def test_get_all_products_success(self, product_service, product_repository, sample_product):
        # Given
        product_repository.find_all.return_value = [sample_product]

        # When
        result = product_service.get_all_products()

        # Then
        assert len(result) == 1
        assert result[0] == sample_product
        product_repository.find_all.assert_called_once() 