import pytest
from decimal import Decimal
from fastapi import status

class TestProductEndpoints:
    @pytest.fixture
    def sample_product_data(self):
        return {
            "name": "Test Product",
            "current_price": "10.00"
        }

    def test_get_products_empty_success(self, client, mock_user, auth_headers):
        # When
        response = client.get(
            "/api/v1/products/",
            headers=auth_headers
        )

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_products_with_data_success(self, client, mock_user, test_session, auth_headers):
        # Given
        from src.product.infrastructure.persistence.postgresql_product_repository import PostgresqlProductRepository
        from src.product.domain.model.product import Product
        
        repository = PostgresqlProductRepository(test_session)
        product = Product.create(
            name="Test Product",
            price=Decimal("10.00")
        )
        saved_product = repository.save(product)

        # When
        response = client.get(
            "/api/v1/products/",
            headers=auth_headers
        )

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == saved_product.name
        assert Decimal(data[0]["current_price"]) == saved_product.current_price.amount

    def test_get_products_unauthorized(self, client):
        # When
        response = client.get("/api/v1/products/")

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "not authenticated" in response.json()["detail"].lower()

    def test_get_products_with_multiple_items_ordered_by_name(self, client, mock_user, test_session, auth_headers):
        # Given
        from src.product.infrastructure.persistence.postgresql_product_repository import PostgresqlProductRepository
        from src.product.domain.model.product import Product
        
        repository = PostgresqlProductRepository(test_session)
        products = [
            Product.create(name="Product B", price=Decimal("15.00")),
            Product.create(name="Product A", price=Decimal("10.00")),
            Product.create(name="Product C", price=Decimal("20.00"))
        ]
        for product in products:
            repository.save(product)

        # When
        response = client.get(
            "/api/v1/products/",
            headers=auth_headers
        )

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        # Verificar que los productos están ordenados por nombre
        assert data[0]["name"] == "Product A"
        assert data[1]["name"] == "Product B"
        assert data[2]["name"] == "Product C"

    def test_get_products_includes_timestamps(self, client, mock_user, test_session, auth_headers):
        # Given
        from src.product.infrastructure.persistence.postgresql_product_repository import PostgresqlProductRepository
        from src.product.domain.model.product import Product
        
        repository = PostgresqlProductRepository(test_session)
        product = Product.create(
            name="Test Product",
            price=Decimal("10.00")
        )
        repository.save(product)

        # When
        response = client.get(
            "/api/v1/products/",
            headers=auth_headers
        )

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert "created_at" in data[0]
        assert "updated_at" in data[0] 