import logging
import os
from logging.handlers import RotatingFileHandler
from core.config import settings

# Logger-Instanz Erstellen
logger = logging.getLogger("recipe-structuring")
logger.setLevel(logging.DEBUG)  # Set to DEBUG for full logs; can be set to INFO or ERROR for production

# Umgebung-basierend log level setting
LOG_LEVEL = settings.LOG_LEVEL
logger.setLevel(getattr(logging, LOG_LEVEL, logging.DEBUG))

# Loggen-Format Einstellen
log_format = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Loggen in Datei
log_file_path = "logs/app.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  # Ensure log directory exists

file_handler = RotatingFileHandler(
    log_file_path, maxBytes=5 * 1024 * 1024, backupCount=5
)
file_handler.setLevel(logging.DEBUG)  # File handler captures all logs (DEBUG and above)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

# Loggen in Console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Console logs can be INFO and above
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)


def get_logger():
    """
    Returns the configured logger instance for use throughout the application.
    """
    return logger
