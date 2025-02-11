from typing import Optional
from src.user.domain.model.user import User
from src.user.domain.repository.user_repository import UserRepository
from src.user.application.dto.user_dto import UserResponseDTO
from src.shared.domain.exceptions import ValidationException
from src.shared.infrastructure.logging.logger import get_logger

logger = get_logger("UserService")

class UserService:
    """Service for user operations"""

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def create_user(self, email: str, name: str) -> UserResponseDTO:
        """Creates a new user"""
        logger.info(f"Creating user with email: {email}")

        # Validate if email already exists
        existing_user = self._repository.find_by_email(email)
        if existing_user:
            logger.warning(f"Attempted to create user with existing email: {email}")
            raise ValidationException(f"Email {email} is already registered")

        try:
            # Create and save user
            user = User.create(email=email, name=name)
            saved_user = self._repository.save(user)
            logger.info(f"User created successfully: {email}")
            return UserResponseDTO.from_entity(saved_user)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}", exc_info=True)
            raise

    def get_user_by_email(self, email: str) -> Optional[UserResponseDTO]:
        """Gets a user by email"""
        user = self._repository.find_by_email(email)
        return UserResponseDTO.from_entity(user) if user else None

    def get_user_id_by_email(self, email: str) -> Optional[int]:
        """Gets a user's ID by email"""
        user = self._repository.find_by_email(email)
        return user.id if user else None
