from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Dict
from src.shared.infrastructure.config.settings import get_settings

settings = get_settings()

class JWTService:
    """Service for handling JWT tokens"""
    
    SECRET_KEY = settings.JWT_SECRET_KEY
    ALGORITHM = settings.JWT_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    @classmethod
    def create_access_token(cls, data: Dict) -> str:
        """Creates a JWT token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({
            "exp": expire,
            "type": "access_token"
        })
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def verify_token(cls, token: str) -> Dict:
        """Verifies a JWT token"""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError:
            raise ValueError("Could not validate credentials") 