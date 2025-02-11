from src.order.domain.service.order_service import OrderService
from src.user.domain.service.user_service import UserService
from src.order.application.dto.order_dto import CreateOrderDTO, OrderResponseDTO
from src.shared.domain.exceptions import ValidationException

class CreateOrderCommand:
    """Command to create a new order"""

    def __init__(self, order_service: OrderService, user_service: UserService):
        self._order_service = order_service
        self._user_service = user_service

    def execute(self, order_data: CreateOrderDTO, waiter_email: str) -> OrderResponseDTO:
        """Executes the order creation command"""
        waiter_id = self._user_service.get_user_id_by_email(waiter_email)
        if not waiter_id:
            raise ValidationException(f"Waiter with email {waiter_email} not found")
            
        order = order_data.to_domain(waiter_id)
        return self._order_service.create_order(order) 