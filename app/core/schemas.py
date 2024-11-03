from pydantic import BaseModel, Field, Json
from typing import Any, Dict


class RecipeRequest(BaseModel):
    """
    Model to validate incoming request data for recipe processing
    """
    recipe_text: str = Field(...,
                             title="Recipe Text",
                             description="Recipe unstructured text")
    schema: Json[Dict[str, Any]] = Field(...,
                                         title="Uploaded Json schema",
                                         description="Recipe JSON schema Input.")


class RecipeResponse(BaseModel):
    """
    JSON Response
    """
    structured_data: Dict[str, Any] = Field(...,
                                            title="Structured Data",
                                            description="Recipe JSON schema Output."
                                            )


class ErrorResponse(BaseModel):
    """
    Error Response
    """
    detail: str = Field(..., title="Error Detail", description="Description of the error.")
