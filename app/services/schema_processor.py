import json
import logging
from typing import Dict, Any
from jsonschema import Draft202012Validator, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SchemaProcessor:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.data = {}
        self.response_schema_key = ""
        self.response_schema = {}
        self.defs = {}
        self.metadata = {}
        self.final_schema = {}

    def load_json(self) -> None:
        """
        Load and validate the input JSON file. Dynamically identify the response schema key.
        """
        try:
            with open(self.input_file, "r") as file:
                self.data = json.load(file)

            # Validate presence of $defs and Metadata
            if "$defs" not in self.data or "Metadata" not in self.data:
                raise KeyError("Input JSON must contain '$defs' and 'Metadata' sections.")

            # Identify the response schema key dynamically
            self.response_schema_key = next(
                key for key in self.data if key not in ["$defs", "Metadata"]
            )
            logging.info(f"Identified response schema key: {self.response_schema_key}")

            self.response_schema = self.data[self.response_schema_key]
            self.defs = self.data["$defs"]
            self.metadata = self.data["Metadata"]

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            logging.error(f"Error loading JSON file: {e}")
            raise

    def apply_metadata(self, schema: Dict[str, Any]) -> None:
        """
        Apply metadata attributes (description, nullable) to schema fields.

        Args:
            schema (dict): The schema to enrich with metadata.
        """
        for field, attributes in self.metadata.items():
            if field in schema:
                if "description" in attributes:
                    schema[field]["description"] = attributes["description"]
                if "nullable" in attributes and attributes["nullable"]:
                    field_type = schema[field].get("type")
                    if isinstance(field_type, list):
                        field_type.append("null")
                    elif field_type:
                        schema[field]["type"] = [field_type, "null"]

    def process_defs(self, schema: Dict[str, Any]) -> None:
        """
        Dynamically replace placeholder fields with $refs pointing to $defs.

        Args:
            schema (dict): The schema to process.
        """
        for key, value in schema.items():
            if isinstance(value, dict):
                for placeholder_key in list(value.keys()):
                    if placeholder_key.endswith("_ref") and placeholder_key.startswith("$"):
                        value["$ref"] = value.pop(placeholder_key)
                self.process_defs(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.process_defs(item)

    def construct_schema(self) -> None:
        """
        Construct the final JSON schema in OpenAI's structured output format.
        """
        self.final_schema = {
            "name": "structured_schema",
            "type": "json_schema",
            "json_schema": {
                "type": "object",
                "properties": self.response_schema,
                "required": list(self.response_schema.keys()),  # Assume all fields are required
                "additionalProperties": False,
            },
            "$defs": self.defs,
        }

    def validate_schema(self) -> None:
        """
        Validate the final schema using JSON Schema Draft 2020-12.
        """
        try:
            Draft202012Validator.check_schema(self.final_schema["json_schema"])
            logging.info("Schema validation successful.")
        except ValidationError as e:
            logging.error(f"Schema validation error: {e}")
            raise

    def save_schema(self) -> None:
        """
        Save the schema to a file in JSON format.
        """
        try:
            with open(self.output_file, "w") as file:
                json.dump(self.final_schema, file, indent=4)
            logging.info(f"Schema saved successfully to '{self.output_file}'.")
        except IOError as e:
            logging.error(f"Failed to save schema: {e}")
            raise

    def process(self) -> None:
        """
        Main orchestration function to load, process, construct, validate, and save the schema.
        """
        try:
            self.load_json()
            self.apply_metadata(self.response_schema)
            self.apply_metadata(self.defs)
            self.process_defs(self.response_schema)
            self.construct_schema()
            self.validate_schema()
            self.save_schema()
        except Exception as e:
            logging.error(f"Error processing schema: {e}")


if __name__ == "__main__":
    # Input and output file paths
    input_file = "/Users/ahmedabouismail/Documents/Uni/Semester_4/FP_ICW/project/recipe-jsons/recipe_v3.json"  # Replace with your input file path
    output_file = "output_schema.json"  # Replace with your desired output file path

    # Create an instance of SchemaProcessor and process the schema
    processor = SchemaProcessor(input_file, output_file)
    processor.process()
