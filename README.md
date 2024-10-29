# Project Setup

## Instructions

Follow these steps to set up the project:

1. **Create a virtual environment:**
   ```sh
   python3 -m venv .venv
   ```

2. **Activate the virtual environment:**
   - On macOS and Linux:
     ```sh
     source .venv/bin/activate
     ```
   - On Windows:
     ```sh
     .venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

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

## Running the FastAPI server

To run the FastAPI server, use the following command:
```sh
uvicorn main:app --reload
```

## Code Coverage Requirements

This project includes code coverage requirements to ensure the quality of the code. To measure code coverage, we use `pytest-cov`.

### Running Tests with Code Coverage

To run the tests and measure code coverage, use the following command:
```sh
pytest --cov=main --cov-report=term-missing
```
