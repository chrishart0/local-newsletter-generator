from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class HelloWorld(BaseModel):
    message: str

def create_hello_world(message: str) -> HelloWorld:
    hello_world = HelloWorld(message=message)
    print(hello_world)
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
    return {"result": divide(a, b)}

# Example usage
create_hello_world("Hello, world!")
print(add(1, 2))
print(subtract(5, 3))
print(multiply(4, 2))
print(divide(10, 2))
