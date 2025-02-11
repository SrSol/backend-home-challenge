from typing import List, Optional
from src.user.domain.model.user import User
from src.user.domain.repository.user_repository import UserRepository
from src.user.application.dto.user_dto import UserResponseDTO
from src.shared.domain.exceptions import ValidationException

class UserService:
    """Service for user operations"""

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def create_user(self, email: str, name: str) -> UserResponseDTO:
        """Creates a new user"""
        # Validate if email already exists
        existing_user = self._repository.find_by_email(email)
        if existing_user:
            raise ValidationException(f"Email {email} is already registered")

        # Create and save user
        user = User.create(email=email, name=name)
        saved_user = self._repository.save(user)
        return UserResponseDTO.from_entity(saved_user)

    def get_user_by_email(self, email: str) -> Optional[UserResponseDTO]:
        """Gets a user by email"""
        user = self._repository.find_by_email(email)
        return UserResponseDTO.from_entity(user) if user else None

    def get_all_users(self) -> List[UserResponseDTO]:
        """Gets all users"""
        users = self._repository.find_all()
        return [UserResponseDTO.from_entity(user) for user in users]

    def get_user_id_by_email(self, email: str) -> Optional[int]:
        """Gets a user's ID by email"""
        user = self._repository.find_by_email(email)
        return user.id if user else None
