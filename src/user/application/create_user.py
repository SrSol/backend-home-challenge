from src.user.domain.service.user_service import UserService
from src.user.application.dto.user_dto import CreateUserDTO, UserResponseDTO

class CreateUserCommand:
    """Command to create a new user"""

    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def execute(self, data: dict) -> UserResponseDTO:
        """Execute the create user command"""
        # Validate input data using CreateUserDTO
        user_dto = CreateUserDTO(**data)

        # Delegate to domain service
        return self._user_service.create_user(
            email=user_dto.email,
            name=user_dto.name
        )
