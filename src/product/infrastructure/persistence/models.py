from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from src.shared.infrastructure.persistence.database import Base

class ProductModel(Base):
    """SQLAlchemy model for Product entity"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    current_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now()) 