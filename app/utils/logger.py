import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.config import settings
from colorama import Fore, Style


class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that applies colors based on log level.
    """

    def format(self, record):
        level_colors = {
            logging.DEBUG: Style.RESET_ALL,  # Default/standard color
            logging.INFO: Fore.GREEN + Style.BRIGHT,  # Green for info
            logging.WARNING: Fore.YELLOW + Style.BRIGHT,  # Yellow for warnings
            logging.ERROR: Fore.RED + Style.BRIGHT,  # Red for errors
        }

        # Apply color to the log level name
        record.levelname = level_colors.get(record.levelno, Style.RESET_ALL) + record.levelname + Style.RESET_ALL
        return super().format(record)


def get_logger(logger_name: str) -> logging.Logger:
    """
    Returns the configured logger instance for use throughout the application.
    """
    # Logger-Instanz Erstellen
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # Set to DEBUG for full logs; can be set to INFO or ERROR for production

    # Umgebung-basierend log level setting
    LOG_LEVEL = settings.log_level
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.DEBUG))

    # Loggen-Format Einstellen
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Loggen in Datei
    log_file_path = "logs/app.log"
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  # Ensure log directory exists

    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)  # File handler captures all logs (DEBUG and above)
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    logger.addHandler(file_handler)

    # Loggen in Console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Console logs INFO and above
    colored_formatter = ColoredFormatter(log_format, datefmt=date_format)
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)

    return logger
