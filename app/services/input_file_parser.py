from app.utils.logger import get_logger
from typing import BinaryIO, Dict, Any, Optional
from app.core.config import settings
import json


class InputFileParser:
    """
    Service class for parsing input files
    """

    def __init__(self):
        self.logger = get_logger("InputFileParser")
        self.logger.info("Initialized InputFileParser")

    def _check_json_obj_depth(self, depth: int) -> bool:
        """
        Checks if the JSON depth is valid.

        Args:
            depth (int): The depth of the JSON object.

        Returns:
            bool: True if the depth is valid, False otherwise.
        """
        if depth <= settings.json_depth and depth != 0:
            return True
        else:
            return False

    def _calculate_json_depth(self, json_dict: Dict[str, Any]) -> int:
        """
        Checks the depth of the JSON object.

        Args:
            json_dict (Dict): The uploaded JSON file.

        Returns:
            int: The depth of the JSON object.
        """
        if isinstance(json_dict, dict):
            return 1 + max((self._calculate_json_depth(value) for value in json_dict.values()), default=0)
        elif isinstance(json_dict, list):
            return 1 + max((self._calculate_json_depth(item) for item in json_dict), default=0)
        else:
            return 0

    def parse_json(self, json_file: BinaryIO) -> Optional[Dict[str, Any]]:
        """
        Parses the input JSON file to a dictionary.
        Args:
            json_file (BinaryIO): The input JSON file
        Returns:
            Dict: The parsed JSON file.
        """
        self.logger.info("Parsing input json file")
        content = json_file.read()
        try:
            json_data = json.loads(content)
            if not isinstance(json_data, dict):
                self.logger.error("JSON root should be an object.")

            depth = self._calculate_json_depth(json_data)
            self.logger.info(f"Response structure depth = {depth}")
            if self._check_json_obj_depth(depth):
                return json_data
            else:
                self.logger.error(
                    f"Depth of the response structure {depth} is invalid.")
                raise Exception(f"Depth of the response structure {depth} is invalid. Valid depth is {settings.json_depth}")
        except json.decoder.JSONDecodeError as e:
            self.logger.error("Invalid uploaded file content")
            raise Exception(f"Invalid uploaded json file: {e}")

    def parse_text(self, text_file: BinaryIO) -> Optional[str]:
        """
        Parses the input text file.
        Args:
            text_file(BinaryIO): The input text file
        Returns:
            str: The parsed content of the text file.
        """

        self.logger.info("Parsing input text file")
        content = str(text_file.read())
        if not isinstance(content, str):
            self.logger.error("Recipe text is not a string")
            return None
        return content

    def _check_if_separators_exist(self, content: str) -> bool:
        """
        Check if the examples separator exists in the content.
        Args:
            content(str): The content to check for the separator.
        Returns:
            bool: True if the separator exists, False otherwise.
        """
        if settings.examples_separator in content:
            return True
        else:
            return False

    def parse_examples(self, examples_file: BinaryIO) -> Optional[str]:
        """
        Parses the input examples file.
        Args:
            examples_file(BinaryIO): The input examples file
        Returns:
            str: The parsed content of the examples file.
        """

        self.logger.info("Parsing input examples file")
        content = str(examples_file.read())
        if not isinstance(content, str):
            self.logger.error("Examples text is not a string")
            return None
        if self._check_if_separators_exist(content):
            content = content.replace(settings.examples_separator, f"\n{settings.examples_separator}\n")
        else:
            self.logger.error("Couldn't find separators in provided examples. Check the Config File")
            raise Exception("Couldn't find separators in provided examples")
        return content