import json
from typing import Dict, Any, Optional
from app.utils.logger import get_logger


class CompletionParser:
    """
    Service to parse completion output
    """

    def __init__(self, completion: str):
        """
        :param completion: The response from the LLM API
        """
        self.completion = completion
        self.logger = get_logger("CompletionParser")
        self.logger.info("Initializing CompletionParser")

    def parse_completion(self) -> Optional[Dict[str, Any]]:
        """
        Parses the LLM API response and returns structured JSON
        :return:  A dictionary representing the structured JSON
        """

        try:
            generated_json = json.loads(self.completion)
            self.logger.info("Successfully parsed generated text into structured JSON data.")
            return generated_json
        except KeyError as e:
            self.logger.error(f"KeyError while parsing completion response: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"JSONDecodeError: Generated text is not valid JSON. Error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error while parsing completion response: {e}")
            return None
