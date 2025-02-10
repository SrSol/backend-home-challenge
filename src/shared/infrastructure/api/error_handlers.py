# File: src/shared/infrastructure/api/error_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from ...domain.exceptions import (
    DomainException,
    EntityNotFoundException,
    ValidationException,
    UnauthorizedException
)

async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

async def not_found_exception_handler(request: Request, exc: EntityNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)}
    )

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)}
    )
