import os
import json

from fastapi import APIRouter, HTTPException, UploadFile, File, Request, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from app.services.prompt_generator import PromptGenerator
from app.services.completion_parser import CompletionParser
from app.services.response_schema_generator import ResponseSchemaGenerator
from app.services.input_file_parser import InputFileParser
from app.services.json_validator import JSONValidator
from tempfile import NamedTemporaryFile
from app.utils.logger import get_logger
from app.services.gpt_service import GPTService
from app.core.config import settings

router = APIRouter()


@router.post("/", summary="Convert unstructured text documents into structured JSON")
async def process_unstructured_text(text_file: UploadFile = File(..., mimetype="text/plain"),
                                    json_file: UploadFile = File(..., media_type="application/json")) -> JSONResponse:
    """
    Processes unstructured text input and validates the output JSON against the user-provided schema.

    Args:
        text_file (UploadFile): File path containing unstructured text.
        json_file (UploadFile): File path for the response schema structure.
    Returns: 
        JSONResponse: Structured Text
    """

    try:
        logger = get_logger("Unstructured Text Processing")
        # Parse uploaded file
        logger.info("Parsing uploaded files")
        file_parser = InputFileParser()
        output_schema = file_parser.parse_json(json_file.file)
        unstructured_text = file_parser.parse_text(text_file.file)

        # Generate response schema
        logger.info("Generating response schema")
        response_schema_generator = ResponseSchemaGenerator()
        response_schema = response_schema_generator.generate_response_schema(output_schema=output_schema)

        # Generate a prompt
        logger.info("Generating prompt for LLM API.")
        prompt_generator = PromptGenerator(unstructured_text)
        prompt = prompt_generator.generate_prompt()

        # Create OpenAI instance and make a request
        logger.info("Making a request to OpenAI")
        gpt_service = GPTService(api_key=settings.llm_api_key)
        gpt_response = gpt_service.complete_prompt(prompt, response_schema)

        # Parse the response
        logger.info("Parsing LLM completion response")
        completion_parser = CompletionParser(gpt_response)
        parsed_response = completion_parser.parse_completion()

        # Validate
        logger.info("Validating JSON structure")
        validator = JSONValidator(parsed_response, output_schema)
        try:
            validator.validate_structure()
            return JSONResponse(parsed_response)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Validation failed{str(e)}")

    except Exception as e:
        logger.error(f"Error processing the unstructured text: {str(e)}")
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
