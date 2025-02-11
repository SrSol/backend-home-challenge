from sqlalchemy import Column, Integer, String, DateTime
from src.shared.infrastructure.persistence.database import Base

class UserModel(Base):
    """SQLAlchemy model for User entity"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
