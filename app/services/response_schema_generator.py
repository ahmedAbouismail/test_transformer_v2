from typing import Dict, Any
from app.utils.logger import get_logger
import json


class ResponseSchemaGenerator:
    def __init__(self) -> None:
        self.logger = get_logger("ResponseSchemaGenerator")

        self.RESPONSE_SCHEMA_KEY = "response_schema"
        self.DEFS_KEY = "$defs"
        self.METADATA_KEY = "metadata"
        self.response_schema = {}
        self.defs = {}
        self.metadata = {}

    def generate_response_schema(self, output_schema: Dict[str, Any]) -> Dict[str, Any]:
        self._split_schema(output_schema)
        inner_schema = self._generate_inner_schema_format(self.response_schema)
        if self.defs:
            self.defs = self._generate_inner_schema_format(self.defs)
            inner_schema = self._add_defs_block(inner_schema)
        if self.metadata:
            inner_schema = self._add_metadata(inner_schema)

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "Recipe",
                "strict": True,
                "schema": inner_schema
            }
        }

        self.logger.info(f"Generated response schema: {response_format}")

        with open('response_schema.json', "w") as rs:
            json.dump(response_format, rs, indent=4)

        return response_format

    def _split_schema(self, output_schema: Dict[str, Any]) -> None:
        self.response_schema = output_schema[self.RESPONSE_SCHEMA_KEY]
        if not self.response_schema:
            raise Exception("No response schema was provided")

        if "$defs" in output_schema.keys():
            self.defs = output_schema[self.DEFS_KEY]
        if "metadata" in output_schema.keys():
            self.metadata = output_schema[self.METADATA_KEY]

    def _add_metadata(self, inner_schema: Dict[str, Any]) -> Dict[str, Any]:
        for field, attributes in self.metadata.items():
            if self._key_exists(field, inner_schema):
                if "description" in attributes.keys():
                    self._search_and_append(field, "description", attributes["description"], inner_schema)
                if "nullable" in attributes.keys():
                    if attributes["nullable"]:
                        self._search_and_append(field, "nullable", attributes["nullable"], inner_schema)
                if "enum" in attributes.keys():
                    self._search_and_append(field, "enum", attributes["enum"], inner_schema)
        return inner_schema

    def _key_exists(self, target_key: str, dictionary: Dict[str, Any]) -> bool:
        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if key == target_key:
                    return True
                elif isinstance(value, dict):
                    if self._key_exists(target_key, value):
                        return True
        return False

    def _search_and_append(self, target_key: str, new_key: str, new_value: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(schema, dict):
            for key, value in schema.items():
                if key == target_key:
                    if isinstance(schema[key], dict):
                        if new_key == "nullable":
                            field_type = schema[target_key].get("type")
                            if field_type:
                                schema[target_key]["type"] = [field_type, "null"]
                        else:
                            schema[key][new_key] = new_value
                    else:
                        raise ValueError(f"The value for '{target_key}' is not a dictionary.")
                elif isinstance(value, dict):
                    self._search_and_append(target_key, new_key, new_value, value)
        return schema

    def _add_defs_block(self, inner_schema: Dict[str, Any]) -> Dict[str, Any]:
        inner_schema[self.DEFS_KEY] = self.defs

        return inner_schema

    def _generate_inner_schema_format(self, output_schema) -> Dict[str, Any]:
        if isinstance(output_schema, dict):
            properties = {}
            required = []

            for key, value in output_schema.items():
                properties[key] = self._generate_inner_schema_format(value)
                required.append(key)

            return {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False
            }
        elif isinstance(output_schema, list):
            if output_schema and isinstance(output_schema[0], dict):
                item_schema = self._generate_inner_schema_format(output_schema[0])
            else:
                item_schema = {"type": "string"}  # default for lists with non-dict items

            return {
                "type": "array",
                "items": item_schema
            }
        elif output_schema.find("$defs") != -1:
            return output_schema
        elif output_schema == "string":
            return {"type": "string"}
        elif output_schema == "integer":
            return {"type": "integer"}
        elif output_schema == "number":
            return {"type": "number"}
        elif output_schema == "boolean":
            return {"type": "boolean"}
        elif output_schema is None:
            return {"type": "null"}
        else:
            return {"type": "string"}