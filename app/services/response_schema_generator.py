from typing import Dict, Any
from app.utils.logger import get_logger


class ResponseSchemaGenerator:
    def __init__(self) -> None:
        self.logger = get_logger("ResponseSchemaGenerator")
        self.inner_schema = {}

    def generate_response_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        inner_schema = self._generate_inner_schema_format(schema)
        response_format = inner_schema
            #{
            # "type": "json_schema",
            # "json_schema": {
            # "name": "Recipe",
            # "strict": True,
            #"schema":

            # }
        #}
        self.logger.info(f"Generated response schema: {response_format}")
        return response_format

    def _generate_inner_schema_format(self, schema: Dict[str, Any]) -> Dict[str, Any]:
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
                #"additionalProperties": False
            }
        elif isinstance(schema, list):
            if schema and isinstance(schema[0], dict):
                item_schema = self._generate_inner_schema_format(schema[0])
            else:
                item_schema = {"type": "string"}  # default for lists with non-dict items

            return {
                "type": "array",
                "items": item_schema
            }
        elif isinstance(schema, str):
            return {"type": "string"}
        elif isinstance(schema, int):
            return {"type": "integer"}
        elif isinstance(schema, float):
            return {"type": "number"}
        elif isinstance(schema, bool):
            return {"type": "boolean"}
        elif schema is None:
            return {"type": "null"}
        else:
            return {"type": "string"}
        # for key, value in schema.items():
        #     if isinstance(value, dict):
        #         nested_properties = self._generate_inner_schema_format(value)
        #         self.inner_schema[key] = {
        #             "type": "object",
        #             "properties": nested_properties,
        #             "required": list(nested_properties.keys()),
        #             "additionalProperties": False
        #         }
        #     elif isinstance(value, list):
        #         if value and isinstance(value[0], dict):
        #             nested_properties = self._generate_inner_schema_format(value[0])
        #             self.inner_schema[key] = {
        #                 "type": "array",
        #                 "items": {
        #                     "type": "object",
        #                     "properties": nested_properties,
        #                     "required": list(nested_properties.keys()),
        #                     "additionalProperties": False
        #                 }
        #             }
        #         else:
        #             item_type = "string" if not value else type(value[0])
        #             self.inner_schema[key] = {
        #                 type: "array",
        #                 "items": {"type": item_type}
        #             }
        #     elif value == "string":
        #         self.inner_schema[key] = {"type": "string"}
        #     elif value == "integer":
        #         self.inner_schema[key] = {"type": "integer"}
        #     elif value == "number":
        #         self.inner_schema[key] = {"type": "number"}
        #     elif value == "float":
        #         self.inner_schema[key] = {"type": "float"}
        #     elif value == "bool":
        #         self.inner_schema[key] = {"type": "boolean"}

        # return self.inner_schema
