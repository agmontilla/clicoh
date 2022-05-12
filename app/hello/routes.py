from fastapi import APIRouter, Depends
from app.auth.routes import auth_handler

hello_router = APIRouter()


@hello_router.get("/", response_model=str)
def hello_world() -> str:
    return "Hello World"


@hello_router.get(
    "/{name}",
    response_model=str,
    dependencies=[Depends(auth_handler.get_current_user)],
)
def hello_name(name: str) -> str:
    return f"Hello {name}, but protected"
