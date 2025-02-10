# File: src/user/domain/service/user_service.py
from typing import Optional
from src.user.domain.model.user import User
from src.user.domain.repository.user_repository import UserRepository
from src.shared.domain.exceptions import ValidationException

class UserService:
    """Domain service for user-related business operations"""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def create_user(self, email: str, name: str) -> User:
        """Creates a new user if email is not already taken"""
        existing_user = self._user_repository.find_by_email(email)
        if existing_user:
            raise ValidationException(f"Email {email} is already registered")
        
        user = User.create(email=email, name=name)
        return self._user_repository.save(user)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieves a user by email"""
        return self._user_repository.find_by_email(email)
