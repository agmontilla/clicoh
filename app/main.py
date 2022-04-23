from fastapi import FastAPI

app = FastAPI()


@app.get("/hello", response_model=str)
def hello_world() -> str:
    return "Hello World"
