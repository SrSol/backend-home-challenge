# File: src/main.py
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.shared.infrastructure.config.settings import get_settings
from src.shared.infrastructure.persistence.database import Base, engine
from src.shared.infrastructure.api.error_handlers import (
    domain_exception_handler,
    not_found_exception_handler,
    unauthorized_exception_handler
)
from src.shared.domain.exceptions import (
    DomainException,
    EntityNotFoundException,
    ValidationException,
    UnauthorizedException
)

# Get settings first
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Configure exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic"""
    errors = exc.errors()
    if errors:
        # Obtener el primer error
        error = errors[0]
        # Extraer el mensaje de error
        detail = error.get("msg", str(exc))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": detail}
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

# Register other exception handlers
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(EntityNotFoundException, not_found_exception_handler)
app.add_exception_handler(ValidationException, validation_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)

# Import routers after configuring exception handlers
from src.user.infrastructure.api.user_routes import router as user_routes

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_routes, prefix=settings.API_V1_STR)
