from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from src.shared.infrastructure.config.settings import get_settings

settings = get_settings()

# Configurar opciones del pool de conexiones
engine = create_engine(
    settings.DB_URL,
    pool_size=settings.DB_POOL_SIZE,               # Tamaño inicial del pool
    max_overflow=settings.DB_MAX_OVERFLOW,         # Conexiones adicionales permitidas
    pool_timeout=settings.DB_POOL_TIMEOUT,         # Tiempo de espera para obtener una conexión
    pool_recycle=settings.DB_POOL_RECYCLE,         # Tiempo para reciclar conexiones
    pool_pre_ping=True,                            # Verificar conexiones antes de usarlas
    poolclass=QueuePool                            # Clase del pool a utilizar
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()