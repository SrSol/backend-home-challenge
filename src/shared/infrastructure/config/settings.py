from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Backend Home Challenge API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "sqlite:///./test.db"
    JWT_SECRET_KEY: str = "your-secret-key-for-testing"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuración del pool de conexiones
    DB_POOL_SIZE: int = 5        # Tamaño del pool (conexiones iniciales)
    DB_MAX_OVERFLOW: int = 10           # Conexiones adicionales permitidas cuando el pool está lleno
    DB_POOL_TIMEOUT: int = 30           # Tiempo máximo de espera para obtener una conexión (en segundos)
    DB_POOL_RECYCLE: int = 1800         # Tiempo para reciclar conexiones (en segundos, 30 minutos)

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
