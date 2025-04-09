from fastapi import APIRouter, Depends, HTTPException, status
from src.user.domain.service.user_service import UserService
from src.auth.infrastructure.jwt_service import JWTService
from src.auth.application.dto.auth_dto import LoginDTO, TokenResponseDTO
from src.shared.infrastructure.api.dependencies import get_user_service

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=TokenResponseDTO)
async def login(
    credentials: LoginDTO,
    user_service: UserService = Depends(get_user_service)
):
    """Login endpoint"""
    user = user_service.get_user_by_email(credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = JWTService.create_access_token({
        "sub": credentials.email,
        "user_id": user.id
    })

    return TokenResponseDTO(
        access_token=token,
        token_type="bearer"
    )
