from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from src.user.domain.model.user import User

class CreateUserDTO(BaseModel):
    """DTO for user creation requests"""
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(
        ...,
        min_length=2,
        error_messages={
            "min_length": "Name must be at least 2 characters long"
        }
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@example.com",
                "name": "Test User"
            }
        }

class UserResponseDTO(BaseModel):
    """DTO for user responses"""
    id: Optional[int]
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_entity(cls, user: User) -> 'UserResponseDTO':
        return cls(
            id=user.id,
            email=str(user.email),
            name=user.name,
            created_at=user.created_at
        )
