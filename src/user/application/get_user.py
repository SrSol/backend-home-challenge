from typing import Optional
from src.user.domain.service.user_service import UserService
from src.user.application.dto.user_dto import UserResponseDTO

class GetUserQuery:
    """Application service for user retrieval"""

    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def execute(self, email: str) -> Optional[UserResponseDTO]:
        """Executes the get user query"""
        user = self._user_service.get_user_by_email(email)
        return UserResponseDTO.from_orm(user) if user else None
