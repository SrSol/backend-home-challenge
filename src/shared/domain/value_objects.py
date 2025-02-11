# File: src/shared/domain/value_objects.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from src.shared.domain.exceptions import ValidationException
import re
from decimal import Decimal
from pydantic import field_validator

class DateTimeRange(BaseModel):
    start_date: datetime
    end_date: datetime

    def __init__(self, **data):
        super().__init__(**data)
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValidationException("Invalid email format")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        # Patrón básico de validación de email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __str__(self):
        return self.value

    def __json__(self):  # Para serialización JSON
        return str(self)

class Money(BaseModel):
    amount: Decimal
    currency: str = "MXN"

    @field_validator('amount', mode='before')
    def validate_amount(cls, v):
        if isinstance(v, str):
            try:
                v = Decimal(v)
            except:
                raise ValueError("Invalid amount format")
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    def __str__(self) -> str:
        return f"{self.amount:.2f}"

    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError("Can only add Money to Money")
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __mul__(self, quantity: int) -> 'Money':
        return Money(amount=self.amount * quantity, currency=self.currency)

    model_config = {
        "json_encoders": {
            Decimal: str
        }
    }
