from core.config import settings
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("Dependencies")


def get_llm_api_key():
    """
    Retrieve the LLM API key from the environment variables
    :raise: HTTPException if the key is not found
    :return: api key
    """
    api_key = settings.llm_api_key
    if not api_key:
        logger.error("LLM API key is missing.")
        raise HTTPException(status_code=500, detail="LLM API key is missing")
    return api_key


def get_logger_dependency():
    """
    Provides consistent logger instance across all endpoints
    :return: logger instance
    """
    return logger
