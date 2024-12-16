from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from app.utils.logger import get_logger


class JSONValidator:

    def __init__(self, parsed_response, output_schema):
        self.parsed_response = parsed_response
        self.output_schema = output_schema
        self.logger = get_logger("JSONValidator")
        self.logger.info("Initializing JSON Validator")

    def validate_structure(self) -> bool:
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
        # Fehlermedlung an LLM senden
