from loguru import logger
import sys
from pathlib import Path
from src.shared.infrastructure.config.settings import get_settings

settings = get_settings()

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure log format
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# Remove default configuration
logger.remove()

# Add console handler in development
if settings.DEBUG:
    logger.add(
        sys.stderr,
        format=log_format,
        level="DEBUG",
        backtrace=True,
        diagnose=True
    )

# Add file handler
logger.add(
    "logs/app.log",
    rotation="500 MB",    # Rotate when reaching 500MB
    retention="10 days",  # Keep logs for 10 days
    compression="zip",    # Compress rotated logs
    format=log_format,
    level="INFO",
    backtrace=True,
    diagnose=True
)

# Add specific handler for errors
logger.add(
    "logs/error.log",
    rotation="100 MB",
    retention="30 days",
    compression="zip",
    format=log_format,
    level="ERROR",
    backtrace=True,
    diagnose=True,
    filter=lambda record: record["level"].name == "ERROR"
)

def get_logger(name: str):
    """Get a logger instance with the given name"""
    return logger.bind(name=name)
