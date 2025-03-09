from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.prompt_generator import PromptGenerator
from app.services.completion_parser import CompletionParser
from app.services.input_file_parser import InputFileParser
from app.services.json_validator import JSONValidator
from app.utils.logger import get_logger
from app.services.gpt_service import GPTService
from app.core.config import settings

router = APIRouter()


@router.post("/", summary="Convert unstructured text documents into structured JSON")
async def process_unstructured_text(examples_file: UploadFile = File(..., media_type="text/plain"),
                                    text_file:     UploadFile = File(..., media_type="text/plain"),
                                    json_file:     UploadFile = File(..., media_type="application/json"),
                                    validation_schema_file:  UploadFile = File(..., media_type="application/json")) -> JSONResponse:
    """
    Processes unstructured text input and validates the output JSON against the user-provided schema.

    Args:
        examples_file (UploadFile): File path containing examples of the structured JSON output.
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
        examples = file_parser.parse_examples(examples_file.file)
        output_schema = file_parser.parse_json(json_file.file)
        unstructured_text = file_parser.parse_text(text_file.file)
        validation_schema = file_parser.parse_validation_schema(validation_schema_file.file)

        # Generate a prompt
        logger.info("Generating prompt for LLM API.")
        prompt_generator = PromptGenerator(unstructured_text, examples)
        prompt = prompt_generator.generate_prompt()

        # Create OpenAI instance and make a request
        logger.info("Making a request to OpenAI")
        gpt_service = GPTService(api_key=settings.llm_api_key)
        gpt_response = gpt_service.complete_prompt(prompt, output_schema)

        # Parse the response
        logger.info("Parsing LLM completion response")
        completion_parser = CompletionParser(gpt_response)
        parsed_response = completion_parser.parse_completion()

        # Validate
        logger.info("Validating JSON structure")
        validator = JSONValidator(parsed_response, validation_schema)
        try:
            validator.validate_structure()
            return JSONResponse(parsed_response)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Validation failed{str(e)}")

    except Exception as e:
        logger.error(f"Error processing the unstructured text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))