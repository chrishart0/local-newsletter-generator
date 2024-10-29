import pytest
from fastapi.testclient import TestClient
from template_python_fastapi_repo.main import (
    app,
    HelloWorld,
    create_hello_world,
    add,
    subtract,
    multiply,
    divide,
    power,
)
from template_python_fastapi_repo.settings import settings
import json

client = TestClient(app)


def test_hello_world_model():
    hello_world = HelloWorld(message="Hello, world!")
    assert hello_world.message == "Hello, world!"


def test_create_hello_world():
    hello_world = create_hello_world("Hello, pytest!")
    assert hello_world.message == "Hello, pytest!"


def test_add():
    assert add(1, 2) == 3


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(4, 2) == 8


def test_divide():
    assert divide(10, 2) == 5

    with pytest.raises(ValueError):
        divide(10, 0)


def test_power():
    assert power(2, 3) == 8


def test_power_endpoint():
    response = client.get("/power?base=2&exponent=3")
    assert response.status_code == 200
    assert response.json() == {"result": 8}


def test_hello_world_endpoint():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}


def test_add_endpoint():
    response = client.get("/add?a=1&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 3}


def test_subtract_endpoint():
    response = client.get("/subtract?a=5&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 2}


def test_multiply_endpoint():
    response = client.get("/multiply?a=4&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 8}


def test_divide_endpoint():
    response = client.get("/divide?a=10&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 5}

    response = client.get("/divide?a=10&b=0")
    assert response.status_code == 400


def test_settings_loaded():
    assert settings.API_KEY == "your_api_key_here"
    assert settings.DATABASE_URL == "your_database_url_here"


def test_stream_endpoint():
    response = client.get("/stream")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    # Capture all messages from the stream and filter out empty lines
    stream_data = [line for line in response.iter_lines() if line.strip()]

    # Log the stream data for debugging
    print("Stream Data:", stream_data)

    # Ensure we have at least two messages
    assert len(stream_data) >= 2, "Not enough messages in the stream"

    # Parse and verify the first message
    first_message = stream_data[0].replace("data: ", "")
    first_data = json.loads(first_message)
    assert first_data["number"] == 1
    assert first_data["message"] == "This is message 1"

    # Parse and verify the second message
    second_message = stream_data[1].replace("data: ", "")
    second_data = json.loads(second_message)
    assert second_data["number"] == 2
    assert second_data["message"] == "This is message 2"


def test_enqueue_task():
    response = client.post("/enqueue-task/", json={"n": 5})
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert "status" in data
    assert data["status"] in ["queued", "started", "finished"]


def test_list_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)


def test_get_task():
    # First, enqueue a task to ensure there's a job to fetch
    enqueue_response = client.post("/enqueue-task/", json={"n": 1})
    assert enqueue_response.status_code == 200
    job_id = enqueue_response.json()["job_id"]

    # Now, fetch the task result
    response = client.get(f"/task/{job_id}")
    assert response.status_code == 200
    task_data = response.json()
    assert task_data["job_id"] == job_id
    assert "result" in task_data


def test_get_non_existent_task():
    response = client.get("/task/non-existent-job-id")
    assert response.status_code == 404
    print(response.json())
