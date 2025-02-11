from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.shared.infrastructure.persistence.database import get_db
from src.shared.infrastructure.api.dependencies import get_current_user
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects import DateTimeRange
from src.order.application.dto.order_dto import CreateOrderDTO, OrderResponseDTO, ProductSalesReportDTO
from src.order.application.create_order import CreateOrderCommand
from src.order.application.get_sales_report import GetSalesReportQuery
from src.order.domain.service.order_service import OrderService
from src.order.infrastructure.persistence.postgresql_order_repository import PostgresqlOrderRepository
from src.user.domain.service.user_service import UserService
from src.user.infrastructure.persistence.postgresql_user_repository import PostgresqlUserRepository
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    repository = PostgresqlOrderRepository(db)
    return OrderService(repository)

def get_order_command(
    db: Session = Depends(get_db)
) -> CreateOrderCommand:
    order_repository = PostgresqlOrderRepository(db)
    order_service = OrderService(order_repository)
    user_repository = PostgresqlUserRepository(db)
    user_service = UserService(user_repository)
    return CreateOrderCommand(order_service, user_service)

@router.post("/", response_model=OrderResponseDTO, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: CreateOrderDTO,
    current_user: str = Depends(get_current_user),
    command: CreateOrderCommand = Depends(get_order_command)
):
    """Creates a new order"""
    try:
        return command.execute(order_data, current_user)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/report", response_model=List[ProductSalesReportDTO])
def get_sales_report(
    current_user: str = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Gets product sales report"""
    try:
        # Si no se proporcionan fechas, usar un rango por defecto
        start_date = datetime.utcnow() - timedelta(days=30)
        end_date = datetime.utcnow()
        date_range = DateTimeRange(start_date=start_date, end_date=end_date)
        
        query = GetSalesReportQuery(order_service)
        return query.execute(date_range)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 