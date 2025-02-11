# File: src/user/domain/model/user.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects import Email

@dataclass(frozen=True)
class User:
    """
    User aggregate root entity representing a waiter in the system.
    Implements business rules and invariants for user creation and validation.
    """
    email: Email
    name: str
    created_at: datetime
    id: Optional[int] = None

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
        if not self.name or len(self.name.strip()) < 2:
            raise ValidationException("Name must be at least 2 characters long")

    @staticmethod
    def create(email: str, name: str) -> 'User':
        """Factory method to create a new user"""
        try:
            email_obj = Email(value=email)
        except ValueError as e:
            raise ValidationException(str(e))

        user = User(
            email=email_obj,
            name=name,
            created_at=datetime.utcnow()
        )
        user._validate()
        return user

    def __str__(self):
        return f"{self.name} <{self.email}>"
