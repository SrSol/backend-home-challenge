from fastapi import FastAPI, Request, status, HTTPException
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
from src.user.infrastructure.api.user_routes import router as user_routes
from src.order.infrastructure.api.order_routes import router as order_routes
from src.auth.infrastructure.api.auth_routes import router as auth_routes

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
    """Handles Pydantic validation errors"""
    errors = exc.errors()
    if errors:
        # Get the first error
        error = errors[0]
        # Extract the error message
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

# Configure specific exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    headers = getattr(exc, "headers", None)
    if exc.status_code == 401:
        if not headers:
            headers = {}
        headers["WWW-Authenticate"] = "Bearer"
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=headers
    )

@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"}
    )

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = await call_next(request)
    # Esto no es estrictamente necesario con FastAPI + Depends,
    # pero puede ser útil para monitoreo
    if hasattr(engine.pool, "status"):
        app.state.db_pool_status = {
            "checkedin": engine.pool.checkedin(),
            "checkedout": engine.pool.checkedout(),
            "size": engine.pool.size(),
            "overflow": engine.pool.overflow()
        }
    return response

# Include routers
app.include_router(user_routes, prefix=settings.API_V1_STR)
app.include_router(order_routes, prefix=settings.API_V1_STR)
app.include_router(auth_routes, prefix=settings.API_V1_STR)
