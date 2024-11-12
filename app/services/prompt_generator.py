import json
from utils.logger import get_logger
from typing import Dict, Any


class PromptGenerator:
    """
    Service class to generate structured prompts for the LLM API based on the input recipe and JSON schema.
    """

    def __init__(self, recipe_text: str):
        """
        :param recipe_text: The unstructured recipe text.
        """
        self.recipe_text = recipe_text
        self.logger = get_logger("PromptGenerator")
        self.logger.info("Initialized PromptGenerator")

    def generate_prompt(self) -> str:
        """
        Generates a prompt for the LLM API to transform the recipe text into a structured JSON format.
        The prompt includes the recipe text and the schema to tell the LLM how the expected output should look like.
        :return: A structured Prompt to send to the LLM API.
        """

        # Build the Prompt
        prompt = (
            #            "Rolle:\n"
            "convert the following unstructured recipe text into a structured JSON format. Notes: input_ingredients: "
            "describes each input ingredient in the step and its state for example: Cooked or raw. "
            "output_ingredients: describes the output ingredients of the step which should be the same input put with "
            "different state. "
            "recipe text: " f"{self.recipe_text}"
            #          "Please return the recipe in JSON format following the response schema."
        )
        self.logger.info("Generated prompt for LLM API.")
        return prompt
