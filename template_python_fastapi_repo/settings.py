from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_KEY: str
    DATABASE_URL: str

    # Use ConfigDict instead of class Config
    model_config = {"env_file": ".env"}


settings = Settings()
