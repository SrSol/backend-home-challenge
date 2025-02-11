# File: src/shared/infrastructure/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.shared.infrastructure.persistence.database import get_db
from src.user.infrastructure.persistence.postgresql_user_repository import PostgresqlUserRepository
from src.user.domain.service.user_service import UserService
from src.auth.infrastructure.jwt_service import JWTService

# Configurar HTTPBearer para devolver 401 en lugar de 403
security = HTTPBearer(
    auto_error=False,  # Cambiar a False para manejar nosotros el error
    description="JWT token required"
)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Gets UserService instance"""
    repository = PostgresqlUserRepository(db)
    return UserService(repository)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service)
) -> str:
    """Gets the current authenticated user"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = JWTService.verify_token(credentials.credentials)
        email = payload.get("sub")
        user_id = payload.get("user_id")
        
        if not email or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = user_service.get_user_by_email(email)
        
        if not user or user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return email
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
