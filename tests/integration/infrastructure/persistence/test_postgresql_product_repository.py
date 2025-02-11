import pytest
from decimal import Decimal
from src.product.domain.model.product import Product
from src.product.infrastructure.persistence.postgresql_product_repository import PostgresqlProductRepository
from src.shared.domain.value_objects import Money

class TestPostgresqlProductRepository:
    @pytest.fixture
    def product_repository(self, test_session):
        return PostgresqlProductRepository(test_session)

    @pytest.fixture
    def sample_product(self):
        return Product.create(
            name="Test Product",
            price=Decimal("10.00")
        )

    def test_save_product_success(self, product_repository, sample_product):
        # When
        saved_product = product_repository.save(sample_product)

        # Then
        assert saved_product.id is not None
        assert saved_product.name == sample_product.name
        assert saved_product.current_price.amount == sample_product.current_price.amount
        assert saved_product.created_at is not None
        assert saved_product.updated_at is not None

    def test_find_by_name_success(self, product_repository, sample_product):
        # Given
        saved_product = product_repository.save(sample_product)

        # When
        found_product = product_repository.find_by_name(saved_product.name)

        # Then
        assert found_product is not None
        assert found_product.id == saved_product.id
        assert found_product.name == saved_product.name

    def test_find_by_name_not_found(self, product_repository):
        # When
        found_product = product_repository.find_by_name("Nonexistent Product")

        # Then
        assert found_product is None

    def test_update_price_success(self, product_repository, sample_product):
        # Given
        saved_product = product_repository.save(sample_product)
        new_price = Decimal("15.00")

        # When
        updated_product = product_repository.update_price(saved_product.id, new_price)

        # Then
        assert updated_product.current_price.amount == new_price
        assert updated_product.id == saved_product.id
        assert updated_product.name == saved_product.name

    def test_find_all_success(self, product_repository, sample_product):
        # Given
        saved_product = product_repository.save(sample_product)

        # When
        products = product_repository.find_all()

        # Then
        assert len(products) == 1
        assert products[0].id == saved_product.id
        assert products[0].name == saved_product.name 