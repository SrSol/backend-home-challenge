from abc import ABC, abstractmethod
from typing import Optional
from src.user.domain.model.user import User

class UserRepository(ABC):
    """Repository interface for User aggregate"""

    @abstractmethod
    def save(self, user: User) -> User:
        """Saves a user and returns the saved entity"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Finds a user by email - needed for duplicate validation"""
        pass
