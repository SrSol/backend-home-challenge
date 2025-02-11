import pytest
from datetime import datetime
from decimal import Decimal
from src.order.application.create_order import CreateOrderCommand
from src.order.application.dto.order_dto import CreateOrderDTO, OrderItemDTO, OrderResponseDTO
from src.order.domain.model.order import Order, OrderItem
from src.shared.domain.value_objects import Money

class TestCreateOrderCommand:
    @pytest.fixture
    def order_service(self, mocker):
        service = mocker.Mock()
        # Configurar el mock para devolver un OrderResponseDTO
        service.create_order.return_value = Order(
            id=1,
            customer_name="Test Customer",
            items=[
                OrderItem(
                    id=1,
                    product_name="Test Product",
                    unit_price=Money(amount=Decimal("10.00")),
                    quantity=2
                )
            ],
            waiter_id=1,
            created_at=datetime.utcnow()
        )
        return service

    @pytest.fixture
    def user_service(self, mocker):
        service = mocker.Mock()
        service.get_user_id_by_email.return_value = 1
        return service

    def test_execute_success(self, order_service, user_service):
        # Given
        command = CreateOrderCommand(order_service, user_service)
        order_data = CreateOrderDTO(
            customer_name="Test Customer",
            items=[
                OrderItemDTO(
                    product_name="Test Product",
                    unit_price=Decimal("10.00"),
                    quantity=2
                )
            ]
        )
        
        # When
        result = command.execute(order_data, "test@example.com")
        
        # Then
        assert isinstance(result, OrderResponseDTO)
        user_service.get_user_id_by_email.assert_called_once_with("test@example.com")
        order_service.create_order.assert_called_once() 