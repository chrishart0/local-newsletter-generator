from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import asyncio
import json
from template_python_fastapi_repo.settings import settings
from template_python_fastapi_repo.helpers.logger_helper import get_logger
from template_python_fastapi_repo.tasks.tasks import (
    example_task,
    get_task_result,
    list_all_jobs,
    queue,
)

app = FastAPI()

# Get the configured logger
logger = get_logger()


class TaskRequest(BaseModel):
    n: int


class HelloWorld(BaseModel):
    message: str


def create_hello_world(message: str) -> HelloWorld:
    hello_world = HelloWorld(message=message)
    logger.info(hello_world)
    return hello_world


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: float, exponent: float) -> float:
    return base**exponent


async def number_generator(iterations: int):
    """Generate numbers from 1 to 10 with a delay."""
    for i in range(1, iterations + 1):
        # Convert data to SSE format
        data = {"number": i, "message": f"This is message {i}"}
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(0.5)  # Wait 1 second between numbers


@app.get("/hello", response_model=HelloWorld)
def hello_world_endpoint():
    return create_hello_world("Hello, world!")


@app.get("/add")
def add_endpoint(a: float, b: float):
    return {"result": add(a, b)}


@app.get("/subtract")
def subtract_endpoint(a: float, b: float):
    return {"result": subtract(a, b)}


@app.get("/multiply")
def multiply_endpoint(a: float, b: float):
    return {"result": multiply(a, b)}


@app.get("/divide")
def divide_endpoint(a: float, b: float):
    try:
        return {"result": divide(a, b)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/power")
def power_endpoint(base: float, exponent: float):
    return {"result": power(base, exponent)}


# You can test this by running `curl http://localhost:8000/stream`
@app.get("/stream")
async def stream_numbers(iterations: int = 2):
    """Endpoint that demonstrates server-sent events (SSE) streaming."""
    return StreamingResponse(
        number_generator(iterations=iterations), media_type="text/event-stream"
    )


@app.post("/enqueue-task/")
def enqueue_task(task_request: TaskRequest):
    """Endpoint to enqueue a task."""
    job = queue.enqueue(example_task, task_request.n)  # Enqueue the task
    return {"job_id": job.id, "status": job.get_status()}


@app.get("/tasks/")
def list_tasks():
    """Endpoint to list all tasks."""
    return list_all_jobs()


@app.get("/task/{job_id}")
def get_task(job_id: str):
    """Endpoint to get the result of a specific task."""
    try:
        result = get_task_result(job_id)
        return {"job_id": job_id, "result": result}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Example usage
create_hello_world("Hello, world!")
logger.info(add(1, 2))
logger.info(subtract(5, 3))
logger.info(multiply(4, 2))
logger.info(divide(10, 2))
logger.info(power(2, 3))

# Use the loaded settings
logger.info(f"API_KEY: {settings.API_KEY}")
logger.info(f"DATABASE_URL: {settings.DATABASE_URL}")
