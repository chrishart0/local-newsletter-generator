from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str

    # Use ConfigDict instead of class Config
    model_config = {"env_file": ".env"}
