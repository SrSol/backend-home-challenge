import pytest
from datetime import datetime
from decimal import Decimal
from src.order.application.create_order import CreateOrderCommand
from src.order.application.dto.order_dto import CreateOrderDTO, OrderItemDTO
from src.order.domain.model.order import Order, OrderItem
from src.shared.domain.value_objects import Money

class TestCreateOrderCommand:
    @pytest.fixture
    def sample_order_dto(self):
        return CreateOrderDTO(
            customer_name="Test Customer",
            items=[
                OrderItemDTO(
                    product_name="Test Product",
                    unit_price=Decimal("10.00"),
                    quantity=2
                )
            ]
        )

    @pytest.fixture
    def mock_order(self):
        return Order(
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

    def test_execute_success(self, mocker, sample_order_dto, mock_order):
        # Given
        mock_service = mocker.Mock()
        mock_service.create_order.return_value = mock_order
        
        command = CreateOrderCommand(mock_service)
        
        # When
        result = command.execute(sample_order_dto, waiter_id=1)
        
        # Then
        assert result.id == mock_order.id
        assert result.customer_name == mock_order.customer_name
        assert len(result.items) == len(mock_order.items)
        assert result.total_price == mock_order.total_price.amount 