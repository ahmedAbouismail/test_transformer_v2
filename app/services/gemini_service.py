import google.generativeai as genai
from app.utils.logger import get_logger
from typing import Dict, Any
from google.generativeai.types import GenerationConfig, BrokenResponseError, IncompleteIterationError
from google.auth.exceptions import DefaultCredentialsError
from google.api_core.exceptions import InvalidArgument, PermissionDenied, ResourceExhausted, AlreadyExists, RetryError


class GeminiService:
    """
    Service for interacting with Gemini API
    """

    def __init__(self,
                 api_key: str,
                 prompt_text: str,
                 response_schema: Dict[str, Any],
                 generative_model: str = "gemini-1.5-pro-latest",
                 max_tokes: int = 500,
                 temperature: float = 0.7,
                 top_p: float = 0.9):
        """
        :param api_key: API key for Gemini API
        :param prompt_text: Text part of the prompt
        :param response_schema: Response schema for structured recipe
        :param generative_model: The name of the model to query
        :param max_tokes: Maximum number of tokens for output
        :param temperature: Controls the randomness of the output
        :param top_p: The maximum cumulative probability of tokens to consider when sampling
        """
        self.logger = get_logger("GeminiService")
        self.gemini = genai

        self.api_key = api_key
        self.prompt_text = prompt_text
        self.response_schema = response_schema
        self.generative_model = generative_model
        self.max_tokes = max_tokes
        self.temperature = temperature
        self.top_p = top_p

        # Call method to initialize the model
        self._set_api_key()
        self.model = self._gemini_model()

        self.logger.info("Initialized Gemini service")

    def _set_api_key(self):
        try:
            self.gemini.configure(api_key=self.api_key)
        except DefaultCredentialsError as e:
            self.logger.error(f"Invalid API key or credentials setup failed: {e}")
            raise

    def _gemini_model(self) -> genai.GenerativeModel:
        return self.gemini.GenerativeModel(self.generative_model)

    def _config_gemini_generation(self) -> GenerationConfig:
        gen_config = GenerationConfig(
            # max_output_tokens=self.max_tokes,
            # temperature=self.temperature,
            # top_p=self.top_p,
            response_mime_type="application/json",
            response_schema=self.response_schema)
        return gen_config

    def complete_prompt(self) -> str:
        """
        Sends the prompt to Gemini API
        :return: Generated response
        """
        try:
            # Send prompt to Gemini
            response = self.model.generate_content(contents=self.prompt_text,
                                                   generation_config=self._config_gemini_generation())
            return response.text
        except InvalidArgument as e:
            self.logger.error(f"Invalid argument in API call: {e}")
            raise
        except PermissionDenied as e:
            self.logger.error(f"Permission denied: {e}")
            raise
        except ResourceExhausted as e:
            self.logger.warning(f"Quota exhausted, retrying: {e}")
            return self._retry_generate()
        except RetryError as e:
            self.logger.error(f"Retry failed: {e}")
            raise
        except BrokenResponseError as e:
            self.logger.error(f"Streaming response error: {e}")
            raise
        except IncompleteIterationError as e:
            self.logger.warning(f"Incomplete response, attempting to resolve: {e}")
            return response.resolve()
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def _retry_generate(self) -> str:
        try:
            # Send prompt to Gemini
            response = self.model.generate_content(contents=self.prompt_text,
                                                   generation_config=self._config_gemini_generation())
            return response.text
        except Exception as e:
            self.logger.error(f"Retry failed: {e}")
            raise
