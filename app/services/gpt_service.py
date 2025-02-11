from openai import (OpenAI, APIError, APIConnectionError, APITimeoutError, AuthenticationError, BadRequestError,
                    ConflictError, InternalServerError, NotFoundError, PermissionDeniedError, RateLimitError,
                    UnprocessableEntityError)
from app.utils.logger import get_logger
from typing import Dict, Any
import time

class GPTService:
    """
    Service for interacting with OpenAI GPT-4 model
    """
    DEFAULT_MODEL = "gpt-4o-2024-08-06"
    DEFAULT_TEMPERATURE = 0
    DEFAULT_TOP_P = 0

    _client_instance = None

    @staticmethod
    def _create_client_instance(api_key: str) -> OpenAI:
        """
        Creates a new instance of the OpenAI client.

        Args:
            api_key (str): The OpenAI API key.

        Returns:
            OpenAIClient: A new instance of the OpenAI client.
        """

        try:
            client = OpenAI(api_key=api_key)
            return client
        except AuthenticationError:
            raise

    def __init__(self, api_key: str):
        """
        Initializes the GPTService instance with an OpenAI client

        Args:
            api_key (str): The OpenAI API key for authenticating API requests.
        """
        self.logger = get_logger("GPTService")
        self.logger.info("Initializing GPTService")

        if not GPTService._client_instance:
            GPTService._client_instance = self._create_client_instance(api_key)
            self.logger.info("Created a new OpenAI client instance")

        self.client = GPTService._client_instance

    def complete_prompt(self, prompt: list[dict], output_format: Dict[str, Any], retries: int = 2,
                        delay: float = 1.0) -> str:
        """
        Sends a prompt to the OpenAI API and retrieves a completion response.

        Args:
            prompt (list[dict]): The prompt data
            output_format (Dict[str, Any]): The format of the expected response.
            retries (int, optional): Number of retry attempts in case of transient API errors. Default is 2.
            delay (float, optional): Delay in seconds between retries. Default is 1.0 Second.

        Returns:
            str: The content of the first choice from the API response.

        Raises:
            Exception: If the maximum retries are exceeded or an unhandled error occurs.
        """
        for attempt in range(retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.DEFAULT_MODEL,
                    temperature=self.DEFAULT_TEMPERATURE,
                    top_p=self.DEFAULT_TOP_P,
                    messages=prompt,
                    response_format=output_format,
                )
                return completion.choices[0].message.content

            except (APITimeoutError, APIConnectionError) as e:
                self.logger.warning(f"Retrying due to transient error: {e} (attempt {attempt + 1})")
                time.sleep(delay)
            except Exception as e:
                self._handle_api_error(e)

    def _handle_api_error(self, error: Exception):
        """
        Handles errors returned by the OpenAI API and logs the error details.

        Args:
            error (Exception): The exception raised by the OpenAI API.

        Raises:
            Exception: Re-raises the exception after logging the error details.
        """
        error_map = {
            BadRequestError: "Invalid request",
            AuthenticationError: "Unauthorized",
            PermissionDeniedError: "Permission denied",
            RateLimitError: "Rate limit exceeded",
            ConflictError: "Conflict error",
            InternalServerError: "Internal server error",
            NotFoundError: "Resource not found",
            UnprocessableEntityError: "Unprocessable entity",
            APIError: "API error",
        }
        error_type = type(error)
        error_message = error_map.get(error_type, "Unknown error")
        self.logger.error(f"OpenAI API error ({error_type}): {error_message} - {error}")
        raise
