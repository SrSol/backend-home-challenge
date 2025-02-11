from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

class ProductResponseDTO(BaseModel):
    """DTO for product responses"""
    id: int
    name: str
    current_price: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 