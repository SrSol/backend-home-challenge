from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.shared.infrastructure.persistence.database import get_db
from src.user.application.dto.user_dto import CreateUserDTO, UserResponseDTO
from src.user.application.create_user import CreateUserCommand
from src.user.domain.service.user_service import UserService
from src.user.infrastructure.persistence.postgresql_user_repository import PostgresqlUserRepository
from src.shared.domain.exceptions import ValidationException

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = PostgresqlUserRepository(db)
    return UserService(repository)

@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: CreateUserDTO,
    user_service: UserService = Depends(get_user_service)
):
    """Creates a new user"""
    try:
        command = CreateUserCommand(user_service)
        return command.execute(user_data.model_dump())
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
