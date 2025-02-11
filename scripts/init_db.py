import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from alembic import command
from alembic.config import Config
from src.shared.infrastructure.config.settings import get_settings

def init_db():
    """Initialize database with migrations and seed data"""
    settings = get_settings()

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    try:
        # Ejecutar todas las migraciones incluyendo el seed data
        command.upgrade(alembic_cfg, "head")
        print("Database initialized successfully with admin user")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()
