# File: src/shared/domain/value_objects.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class DateTimeRange(BaseModel):
    start_date: datetime
    end_date: datetime

    def __init__(self, **data):
        super().__init__(**data)
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")

class Email(BaseModel):
    value: EmailStr

    def __str__(self):
        return self.value

    def model_dump(self, **kwargs):
        return self.value

class Money(BaseModel):
    amount: float
    currency: str = "MXN"

    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __mul__(self, quantity: int) -> 'Money':
        return Money(amount=self.amount * quantity, currency=self.currency)
