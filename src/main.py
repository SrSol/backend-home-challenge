# File: src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.shared.infrastructure.config.settings import get_settings
from src.shared.infrastructure.persistence.database import Base, engine
from src.shared.infrastructure.api.error_handlers import (
    domain_exception_handler,
    not_found_exception_handler,
    validation_exception_handler,
    unauthorized_exception_handler
)
from src.shared.domain.exceptions import (
    DomainException,
    EntityNotFoundException,
    ValidationException,
    UnauthorizedException
)

# Create database tables
Base.metadata.create_all(bind=engine)

settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(EntityNotFoundException, not_found_exception_handler)
app.add_exception_handler(ValidationException, validation_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)

# Include routers
# Will be added as we implement each domain module
