import pytest
from fastapi.testclient import TestClient
from main import app, HelloWorld, create_hello_world, add, subtract, multiply, divide
from settings import settings

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
