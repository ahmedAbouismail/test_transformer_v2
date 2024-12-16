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
        Checks if the json depth is valid
        :param depth: depth of the json object
        :return: True if valid, False otherwise
        """
        if depth <= settings.json_depth and depth != 0:
            return True
        else:
            return False

    def _calculate_json_depth(self, json_dict: Dict[str, Any]) -> int:
        """
        Checks the depth of the JSON Obj
        :param json_dict:Uploaded json file
        :return: depth of the JSON Obj
        """
        if isinstance(json_dict, dict):
            return 1 + max((self._calculate_json_depth(value) for value in json_dict.values()), default=0)
        elif isinstance(json_dict, list):
            return 1 + max((self._calculate_json_depth(item) for item in json_dict), default=0)
        else:
            return 0

    def parse_json(self, json_file: BinaryIO) -> Optional[Dict[str, Any]]:
        """
        Parse input json file to dict type
        :return: parsed json file
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
        except json.decoder.JSONDecodeError:
            self.logger.error("Invalid uploaded file content")
        return None

    def parse_text(self, text_file: BinaryIO) -> Optional[str]:
        """
        Parse input text file
        :return: parsed text file
        """
        self.logger.info("Parsing input text file")
        content = str(text_file.read())
        if not isinstance(content, str):
            self.logger.error("Recipe text is not a string")
            return None
        return content
