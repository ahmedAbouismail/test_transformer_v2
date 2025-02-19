from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """"
    Config Settings for the Unstructured Documents Structuring App
    Settings are loaded from the .env
    """

    # Application settings
    app_name: str = Field("Unstructured Documents Structuring", env="APP_NAME")
    app_version: str = Field("1.0.0", env="")

    # LLM API Settings
    llm_api_key: str = Field(..., env="LLM_API_KEY", description="LLM API Key for accessing the LLM service")

    # Logging settings
    log_level: str = Field("DEBUG", env="LOG_LEVEL", description="Logging level")

    # Response structure rules
    json_depth: int = Field("5", env="JSON_DEPTH", description="Allowed JSON depth")

    examples_separator: str = Field("===", env="EXAMPLES_SEPARATOR", description="Separator for examples in the prompt")


settings = Settings()
