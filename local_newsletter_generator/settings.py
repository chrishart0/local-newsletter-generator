from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Any, Optional

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_DEPLOYMENT_NAME: Optional[str] = None

    model_config = {"env_file": ".env"}

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.OPENAI_API_KEY and not (
            self.AZURE_OPENAI_API_KEY
            and self.AZURE_OPENAI_ENDPOINT
            and self.AZURE_OPENAI_DEPLOYMENT_NAME
        ):
            raise ValueError(
                "Either OPENAI_API_KEY is required or all 3 Azure parameters are required"
            )
