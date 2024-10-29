from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    API_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
