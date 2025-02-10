# File: src/user/application/create_user.py
from src.user.domain.service.user_service import UserService
from src.user.application.dto.user_dto import CreateUserDTO, UserResponseDTO

class CreateUserCommand:
    """Application service for user creation"""

    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def execute(self, user_dto: CreateUserDTO) -> UserResponseDTO:
        """Executes the user creation command"""
        user = self._user_service.create_user(
            email=user_dto.email,
            name=user_dto.name
        )
        return UserResponseDTO.from_orm(user)
