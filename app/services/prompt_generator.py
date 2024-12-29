from typing import List, Union, Dict

from app.utils.logger import get_logger


class PromptGenerator:
    """
    Service class to generate structured prompts for the LLM API based on the input recipe and JSON schema.
    """

    def __init__(self, unstructured_text: str):
        """
        Args: 
            unstructured_text (str): the input unstructured text to convert
        """
        self.unstructured_text = unstructured_text
        self.logger = get_logger("PromptGenerator")
        self.logger.info("Initialized PromptGenerator")

    def generate_prompt(self) -> list:
        """
        Generates a prompt for the LLM API to transform the recipe text into a structured JSON format.

        The prompt includes the recipe text and the schema to instruct the LLM on the expected output format.

        Returns:
            str: A structured prompt to send to the LLM API.
        """
        prompt = [
            {
                "role": "system",
                "content": "You are a data extraction assistant specializing in transforming unstructured text into "
                           "structured JSON formats. Your task is to extract information from the provided text and "
                           "organize it into a structured JSON format following the provided JSON schema. Ensure all "
                           "extracted information matches the structure and data types defined in the schema.\n\n"
                           ""
                           "Before extracting information, apply named entity recognition to identify relevant "
                           "entities and relationship extraction techniques to map connections between entities. Use "
                           "these insights to populate the JSON schema fields accurately.\n\n"
                           ""
                           "If a value for any key in the schema is not present in the text or cannot be confidently "
                           "inferred, return null for that key. For example, if the text does not include a required "
                           "\n\n"
                           ""
                           "Input: \n"
                           "- Text: A block of unstructured text.\n"
                           "- Schema: A JSON schema defining the expected keys and data types.\n\n"
                           ""
                           "Output: \n"
                           "- A JSON object populated with data extracted from the text.\n\n"
                           ""
            },
            {
                "role": "user",
                "content": f"{self.unstructured_text}"
            }
        ]
        self.logger.info("Generated prompt for LLM API.")

        return prompt
