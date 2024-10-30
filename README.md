# Template Python FastAPI Repo
[![CI](https://github.com/chrishart0/local-newsletter-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/chrishart0/local-newsletter-generator/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/chrishart0/local-newsletter-generator/graph/badge.svg?token=6QFK2BOQ54)](https://codecov.io/github/chrishart0/local-newsletter-generator)

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

4. **Install dependencies with Poetry:**
   Check if you have poetry by running `poetry --version`

   If you don't have poetry, go install it: <https://python-poetry.org/docs/>

   ```sh
   poetry install
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
uvicorn local_newsletter_generator.main:app --reload
```

Now navigate to <http://127.0.0.1:8000/docs> and you will see the running FastAPI OpenAI spec

## Testing

This project includes code coverage requirements to ensure the quality of the code. To measure code coverage, we use `pytest-cov`.

### Running Tests with Code Coverage

To run the tests and measure code coverage, use the following command:
```sh
poetry run pytest --cov --cov-report=term-missing
```

## Linting

```bash
poetry run black .
poetry run flake8 .
```

## Environment Variables

This project uses environment variables to manage sensitive information and configuration settings. Follow these steps to set up and use the environment variables:

1. **Create a `.env` file:**
   Create a `.env` file in the root of the repository with the following content:
   ```sh
   API_KEY=your_api_key_here
   DATABASE_URL=your_database_url_here
   ```

2. **Run the needed services:**
   ```sh
   docker-compose up -d
   ```

2. **Run the FastAPI server:**
   Use the following command to run the FastAPI server:
   ```sh
   uvicorn local_newsletter_generator.main:app --reload
   ```
3. **Verify the settings:**
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

# Application Architecture

1) A system for taking in raw data about events happening which extracts events and stores them in a structured way
2) A system which parses through the events to assemble highlights