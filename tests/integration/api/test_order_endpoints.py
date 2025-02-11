import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from fastapi import status
from src.order.domain.model.order import Order, OrderItem
from src.shared.domain.value_objects import Money
from src.order.infrastructure.persistence.postgresql_order_repository import PostgresqlOrderRepository

class TestOrderEndpoints:
    @pytest.fixture
    def sample_order_data(self):
        return {
            "customer_name": "Test Customer",
            "items": [
                {
                    "product_name": "Test Product 1",
                    "unit_price": "10.00",
                    "quantity": 2
                },
                {
                    "product_name": "Test Product 2",
                    "unit_price": "15.00",
                    "quantity": 1
                }
            ]
        }

    def test_create_order_success(self, client, sample_order_data, test_user, auth_headers):
        # When
        response = client.post(
            "/api/v1/orders/",
            json={
                "customer_name": sample_order_data["customer_name"],
                "items": [
                    {
                        "product_name": item["product_name"],
                        "unit_price": str(item["unit_price"]),
                        "quantity": item["quantity"]
                    }
                    for item in sample_order_data["items"]
                ]
            },
            headers=auth_headers
        )

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["customer_name"] == sample_order_data["customer_name"]
        assert len(data["items"]) == len(sample_order_data["items"])
        assert "id" in data
        assert "created_at" in data
        assert data["total_price"] == "35.00"  # 2*10 + 1*15
        assert "waiter_id" in data
        assert data["waiter_id"] == test_user.id

    @pytest.mark.parametrize("invalid_data,expected_detail", [
        (
            {"items": []},
            "field required"
        ),
        (
            {"customer_name": "", "items": []},
            "string should have at least 2 characters"
        ),
        (
            {
                "customer_name": "Test",
                "items": [{"product_name": "P1", "unit_price": "0", "quantity": 1}]
            },
            "unit price must be greater than 0"
        ),
    ])
    def test_create_order_validation_error(self, client, invalid_data, expected_detail, test_user, auth_headers):
        # When
        response = client.post(
            "/api/v1/orders/",
            json=invalid_data,
            headers=auth_headers
        )

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_detail.lower() in response.json()["detail"].lower()

    def test_get_sales_report_success(self, client, test_user, test_db, auth_headers):
        # Given
        # Crear algunas órdenes de prueba
        repository = PostgresqlOrderRepository(test_db)
        order = Order.create(
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
            waiter_id=test_user.id
        )
        repository.save(order)
        test_db.commit()

        # When
        response = client.get(
            "/api/v1/orders/report",
            headers=auth_headers
        )

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert data[0]["product_name"] == "Test Product 1"
        assert data[0]["total_quantity"] == 2
        assert data[0]["total_price"] == "20.00" 