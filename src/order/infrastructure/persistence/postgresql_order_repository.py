from typing import Optional, List
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from src.order.domain.model.order import Order, OrderItem
from src.order.domain.repository.order_repository import OrderRepository
from src.order.infrastructure.persistence.models import OrderModel, OrderItemModel
from src.shared.domain.value_objects import Money

class PostgresqlOrderRepository(OrderRepository):
    """PostgreSQL implementation of OrderRepository"""

    def __init__(self, session: Session):
        self._session = session

    def save(self, order: Order) -> Order:
        order_model = OrderModel(
            customer_name=order.customer_name,
            waiter_id=order.waiter_id,
            created_at=order.created_at,
            items=[
                OrderItemModel(
                    product_name=item.product_name,
                    unit_price=item.unit_price.amount,
                    quantity=item.quantity
                )
                for item in order.items
            ]
        )
        
        self._session.add(order_model)
        self._session.commit()
        self._session.refresh(order_model)
        
        return self._order_model_to_entity(order_model)

    def find_by_id(self, id: int) -> Optional[Order]:
        order_model = self._session.query(OrderModel).filter(
            OrderModel.id == id
        ).first()
        return self._order_model_to_entity(order_model) if order_model else None

    def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Order]:
        order_models = self._session.query(OrderModel).filter(
            OrderModel.created_at.between(start_date, end_date)
        ).all()
        return [self._order_model_to_entity(om) for om in order_models]

    def get_product_sales_report(self, start_date: datetime, end_date: datetime) -> List[dict]:
        report = self._session.query(
            OrderItemModel.product_name,
            func.sum(OrderItemModel.quantity).label("total_quantity"),
            func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).label("total_price")
        ).join(OrderModel).filter(
            OrderModel.created_at.between(start_date, end_date)
        ).group_by(
            OrderItemModel.product_name
        ).order_by(
            func.sum(OrderItemModel.quantity).desc()
        ).all()

        return [
            {
                "product_name": r.product_name,
                "total_quantity": r.total_quantity,
                "total_price": r.total_price
            }
            for r in report
        ]

    def _order_model_to_entity(self, order_model: OrderModel) -> Order:
        """Converts OrderModel to Order domain entity"""
        return Order(
            id=order_model.id,
            customer_name=order_model.customer_name,
            waiter_id=order_model.waiter_id,
            created_at=order_model.created_at,
            items=[
                OrderItem(
                    id=item.id,
                    product_name=item.product_name,
                    unit_price=Money(amount=item.unit_price),
                    quantity=item.quantity
                )
                for item in order_model.items
            ]
        ) 