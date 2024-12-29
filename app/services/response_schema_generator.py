from typing import Dict, Any
from app.utils.logger import get_logger
import json


class ResponseSchemaGenerator:
    """
    Generates OpenAI-compatible response schemas from input schemas.
    """

    RESPONSE_SCHEMA_KEY = "response_schema"
    DEFS_KEY = "$defs"
    METADATA_KEY = "metadata"

    def __init__(self) -> None:
        self.logger = get_logger("ResponseSchemaGenerator")
        self.response_schema = None
        self.defs = None
        self.metadata = None

    def generate_response_schema(self, output_schema: Dict[str, Any], schema_name: str = "Schema",
                                 output_file: str = "response_schema.json") -> Dict[str, Any]:
        """
        Generates a structured JSON schema and saves it to a file.

        Args:
            output_schema (Dict[str, Any]): The input schema to process.
            output_file (str): The file path to save the generated schema.
            schema_name (str): Name of the schema
        Returns:
            Dict[str, Any]: The generated response schema.
        """
        self._split_schema(output_schema)
        inner_schema = self._generate_inner_schema_format(self.response_schema)

        if self.defs:
            self.defs = self._generate_inner_schema_format(self.defs)
            inner_schema = self._add_defs_block(inner_schema)

        if self.metadata:
            inner_schema = self._add_metadata(inner_schema)

        response_format = self._build_response_format(inner_schema, schema_name)
        self._save_schema_to_file(response_format, output_file)

        self.logger.info(f"Generated response schema saved to {output_file}")
        return response_format

    def _build_response_format(self, schema: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
        """
        Builds the final response format.

        Args:
            schema (Dict[str, Any]): The processed schema.

        Returns:
            Dict[str, Any]: The response format.
        """
        return {
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "strict": True,
                "schema": schema
            }
        }

    def _save_schema_to_file(self, schema: Dict[str, Any], filename: str) -> None:
        """
        Saves the generated schema to a file.

        Args:
            schema (Dict[str, Any]): The schema to save.
            filename (str): The file path to save the schema.
        """
        with open(filename, "w") as file:
            json.dump(schema, file, indent=4)

    def _split_schema(self, output_schema: Dict[str, Any]) -> None:
        """
        Splits the input schema into components: response schema, defs, and metadata.

        Args:
            output_schema (Dict[str, Any]): The input schema to split.

        Raises:
            KeyError: If the required response schema is missing.
        """
        try:
            self.response_schema = output_schema[self.RESPONSE_SCHEMA_KEY]
        except KeyError:
            raise KeyError(f"Missing required key: {self.RESPONSE_SCHEMA_KEY}")

        self.defs = output_schema.get(self.DEFS_KEY, {})
        self.metadata = output_schema.get(self.METADATA_KEY, {})

    def _add_metadata(self, inner_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds metadata attributes (e.g., descriptions, nullable, enums) to the schema.

        Args:
            inner_schema (Dict[str, Any]): The schema to modify.

        Returns:
            Dict[str, Any]: The schema with metadata added.
        """
        for field, attributes in self.metadata.items():
            if self._key_exists(field, inner_schema):
                for key, value in attributes.items():
                    if key in {"description", "nullable", "enum"}:
                        self._search_and_append(field, key, value, inner_schema)
        return inner_schema

    def _key_exists(self, target_key: str, schema: Dict[str, Any]) -> bool:
        """
        Recursively checks if a key exists in the schema.

        Args:
            target_key (str): The key to check.
            schema (Dict[str, Any]): The schema to search.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        if isinstance(schema, dict):
            for key, value in schema.items():
                if key == target_key:
                    return True
                elif isinstance(value, dict) and self._key_exists(target_key, value):
                    return True
        return False

    def _search_and_append(self, target_key: str, new_key: str, new_value: str, schema: Dict[str, Any]) -> Dict[
        str, Any]:
        """
        Recursively appends new attributes (e.g., description, nullable) to a field.

        Args:
            target_key (str): The key of the field to modify.
            new_key (str): The attribute to add.
            new_value (Any): The value of the new attribute.
            schema (Dict[str, Any]): The schema to modify.
        """

        if isinstance(schema, dict):
            for key, value in schema.items():
                if key == target_key:
                    if isinstance(schema[key], dict):
                        if new_key == "nullable":
                            self._handle_nullable(schema[key])
                        schema[key][new_key] = new_value
                    elif isinstance(value, dict):
                        self._search_and_append(target_key, new_key, new_value, value)

    def _handle_nullable(self, target_schema: Dict[str, Any]) -> None:
        """
        Modifies the schema to make a field nullable.

        Args:
            target_schema (Dict[str, Any]): The schema of the field to modify.
        """
        field_type = target_schema.get("type")
        if field_type:
            target_schema["type"] = [field_type, "null"]

    def _add_defs_block(self, inner_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds reusable `$defs` to the schema.

        Args:
            inner_schema (Dict[str, Any]): The schema to modify.

        Returns:
            Dict[str, Any]: The schema with `$defs` added.
        """
        inner_schema[self.DEFS_KEY] = self.defs
        return inner_schema

    def _generate_inner_schema_format(self, schema: Any) -> Dict[str, Any]:
        """
        Recursively formats the schema to include type definitions and validation.

        Args:
            schema (Any): The input schema to format.

        Returns:
            Dict[str, Any]: The formatted schema.
        """

        if isinstance(schema, dict):
            properties = {}
            required = []

            for key, value in schema.items():
                properties[key] = self._generate_inner_schema_format(value)
                required.append(key)

            return {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False
            }
        elif isinstance(schema, list):
            item_schema = self._generate_inner_schema_format(schema[0]) if schema else {"type": "string"}
            return {"type": "array", "items": item_schema}
        elif schema in {"string", "integer", "number", "boolean", None}:
            return {"type": schema or "null"}
        else:
            return {"type": "string"}
