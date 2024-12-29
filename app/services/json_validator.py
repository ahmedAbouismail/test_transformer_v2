from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from app.utils.logger import get_logger
from typing import Dict, Any

class JSONValidator:

    def __init__(self, parsed_response: Dict[str, Any], output_schema: Dict[str, Any]):
        """
        Initializes the JSONValidator with the parsed JSON response and the schema.

        Args:
            parsed_response (DictDict[str, Any]): The JSON response to be validated.
            output_schema (DictDict[str, Any]): The schema to validate the response against.
        """
        self.parsed_response = parsed_response
        self.output_schema = output_schema
        self.logger = get_logger("JSONValidator")
        self.logger.info("Initializing JSON Validator")

    def validate_structure(self) -> bool:
        """
        Validates the structure of the parsed JSON response against the output schema.

        Returns:
            bool: True if the JSON response is valid, otherwise raises an exception.

        Raises:
            Exception: If the parsed response or schema is invalid, or an unexpected error occurs.
        """
        try:
            validate(instance=self.parsed_response, schema=self.output_schema)
            return True
        except ValidationError as e:
            self.logger.error(f"The parsed response is invalid. Error: {e.message}")
            raise Exception(f"The parsed response is invalid. Error: {e.message}")
        except SchemaError as e:
            self.logger.error(f"The output schema is invalid. Error: {e.message}")
            raise Exception(f"The parsed response is invalid. Error: {e.message}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise Exception(str(e))
