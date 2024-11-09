from utils.logger import get_logger
from typing import BinaryIO, Dict, Any, Optional
import json


class InputFileParser:
    """
    Service class for parsing input files
    """
    def __init__(self, text_file: BinaryIO, json_file: BinaryIO):
        """
        :param text_file: Uploaded text file
        :param json_file: Uploaded json file
        """
        self.logger = get_logger("InputFileParser")
        self.text_file = text_file
        self.json_file = json_file
        self.logger.info("Initialized InputFileParser")

    def parse_json(self) -> Optional[Dict[str, Any]]:
        """
        Parse input json file to dict type
        :return: parsed json file
        """
        self.logger.info("Parsing input json file")
        content = self.json_file.read()
        try:
            json_data = json.loads(content)
            if not isinstance(json_data, dict):
                self.logger.error("JSON root should be an object.")
            return json_data
        except json.decoder.JSONDecodeError:
            self.logger.error("Invalid uploaded file content")
        return None

    def parse_text(self) -> Optional[str]:
        """
        Parse input text file
        :return: parsed text file
        """
        self.logger.info("Parsing input text file")
        content = str(self.text_file.read())
        if not isinstance(content, str):
            self.logger.error("Recipe text is not a string")
            return None
        return content
