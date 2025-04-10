from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from src.shared.infrastructure.config.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.DB_URL,
    pool_size=settings.DB_POOL_SIZE,               # Initial size of the pool
    max_overflow=settings.DB_MAX_OVERFLOW,         # Additional connections allowed
    pool_timeout=settings.DB_POOL_TIMEOUT,         # Wait time to establish a connection
    pool_recycle=settings.DB_POOL_RECYCLE,         # Time to recycle connections
    pool_pre_ping=True,                            # Validate connections before use
    poolclass=QueuePool                            # Pool Class to use
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
