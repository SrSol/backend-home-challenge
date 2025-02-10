# File: src/user/application/dto/user_dto.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

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
    id: int
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        obj_dict = {
            'id': obj.id,
            'email': str(obj.email),
            'name': obj.name,
            'created_at': obj.created_at
        }
        return cls(**obj_dict)

