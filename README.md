# Template Python FastAPI Repo
[![CI](https://github.com/chrishart0/template-python-fastapi-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/chrishart0/template-python-fastapi-repo/actions/workflows/ci.yml)

## Instructions

Follow these steps to set up the project:

1. **Set up Python version with pyenv:**
   *Install pyenv if you don't have it: <https://github.com/pyenv/pyenv>*

   ```sh
   # Install specific Python version
   pyenv install 3.12
   pyenv local 3.12
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On macOS and Linux:
     ```sh
     source .venv/bin/activate
     ```
   - On Windows:
     ```sh
     .venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

5. **Setup your .env**
Copy the `.env.example` file to `.env` and update the values:

6. **Optional: Setup pre-commit hook**
```
pre-commit install
```

## Running the FastAPI server

To run the FastAPI server, use the following command:
```sh
uvicorn main:app --reload
```

## Testing

This project includes code coverage requirements to ensure the quality of the code. To measure code coverage, we use `pytest-cov`.

### Running Tests with Code Coverage

To run the tests and measure code coverage, use the following command:
```sh
pytest --cov=main --cov-report=term-missing
```

## Linting

```bash
python -m black .
```

## Environment Variables

This project uses environment variables to manage sensitive information and configuration settings. Follow these steps to set up and use the environment variables:

1. **Create a `.env` file:**
   Create a `.env` file in the root of the repository with the following content:
   ```sh
   API_KEY=your_api_key_here
   DATABASE_URL=your_database_url_here
   ```

2. **Create a `settings.py` file:**
   Create a `settings.py` file in the root of the repository with the following content:
   ```python
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
   ```

3. **Update `main.py` to use the settings:**
   Import the `Settings` class from `settings.py` and use the loaded settings in the FastAPI app. For example:
   ```python
   from settings import settings

   # Use the loaded settings
   print(f"API_KEY: {settings.API_KEY}")
   print(f"DATABASE_URL: {settings.DATABASE_URL}")
   ```

4. **Run the FastAPI server:**
   Use the following command to run the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```

5. **Verify the settings:**
   Ensure that the environment variables are loaded correctly by checking the output of the FastAPI server or running the tests.

## Basic Pydantic Model

This project includes a basic Pydantic model to validate and serialize data.

### HelloWorld Model

The `HelloWorld` model has the following field:
- `message`: a string representing the message

### Example Usage

Here's an example of how to create a `HelloWorld` instance and print it:

```python
from pydantic import BaseModel

class HelloWorld(BaseModel):
    message: str

def create_hello_world(message: str) -> HelloWorld:
    hello_world = HelloWorld(message=message)
    print(hello_world)
    return hello_world

# Example usage
create_hello_world("Hello, World!")
```