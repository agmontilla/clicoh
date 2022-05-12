from fastapi import FastAPI
from app.hello.routes import hello_router
from app.auth.routes import auth_router

app = FastAPI()

app.include_router(hello_router, prefix="/hello", tags=["Hello"])
app.include_router(auth_router, prefix="/users", tags=["Auth"])
