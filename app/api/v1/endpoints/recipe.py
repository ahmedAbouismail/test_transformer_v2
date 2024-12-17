import os
import json

from fastapi import APIRouter, HTTPException, UploadFile, File, Request, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from app.services.gemini_service import GeminiService
from app.services.prompt_generator import PromptGenerator
from app.services.completion_parser import CompletionParser
from app.services.response_schema_generator import ResponseSchemaGenerator
from app.services.input_file_parser import InputFileParser
from app.services.json_validator import JSONValidator
from tempfile import NamedTemporaryFile
from app.utils.logger import get_logger

router = APIRouter()


@router.post("/", summary="Convert unstructured recipe data to text into structured JSON")
async def process_recipe(text_file: UploadFile = File(..., mimetype="text/plain"),
                         json_file: UploadFile = File(..., media_type="application/json")):
    """
     Processes unstructured recipe text input and validates the output JSON against the user provided schema
    :param text_file: Text file with unstructured recipe text
    :param json_file: Json file for the response schema structure
    :param llm_api_key: Injected by get_llm_api_key key to access the LLM API
    :param logger: Injected by get_logger_dependency for consistent logging across the endpoint
    :return: RecipeResponse object
    """

    try:
        logger = get_logger("Recipe Processing")
        # Parse uploaded file
        logger.info("Parsing uploaded files")
        file_parser = InputFileParser()
        output_schema = file_parser.parse_json(json_file.file)
        recipe_text = file_parser.parse_text(text_file.file)

        # Generate response schema
        logger.info("Generating response schema")
        response_schema_generator = ResponseSchemaGenerator()
        response_schema = response_schema_generator.generate_response_schema(output_schema)

        # TODO: Chunk of big texts
        # Generate a prompt
        logger.info("Generating prompt for LLM API.")
        prompt_generator = PromptGenerator(recipe_text)
        prompt = prompt_generator.generate_prompt()

        # Send the prompt to the LLM API
        logger.info("Sending prompt to Gemini API")
        gemini_service = GeminiService(prompt_text=prompt,
                                       response_schema=response_schema)
        completion = gemini_service.complete_prompt()

        # Parse the response
        logger.info("Parsing LLM completion response")
        completion_parser = CompletionParser(completion)
        parsed_response = completion_parser.parse_completion()

        # Validate
        logger.info("Validating JSON structure")
        validator = JSONValidator(parsed_response, output_schema)
        try:
            is_valid = validator.validate_structure()
            return JSONResponse(parsed_response)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Validation failed{str(e)}")

    except Exception as e:
        logger.error(f"Error processing recipe: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/download", summary="Endpoint to download the processed JSON response as a file")
async def download_structured_recipe(request: Request, background_tasks: BackgroundTasks):
    """
    Endpoint to download the processed JSON response as a file
    :param request: Request body
    :param background_tasks: Background task to delete the temporary file after download
    :return: File as a downloadable response
    """
    response_data = await request.json()

    with NamedTemporaryFile(delete=False, suffix=".json", mode="w") as temp_file:
        json.dump(response_data, temp_file)
        temp_file_path = temp_file.name

    background_tasks.add_task(lambda: os.remove(temp_file_path))

    return FileResponse(path=temp_file_path,
                        media_type="application/json",
                        filename="structured_recipe.json")
