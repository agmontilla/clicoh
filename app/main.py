from fastapi import FastAPI, Depends
from app.hello.routes import hello_router
from app.auth.routes import auth_router
from app.products.routes import products_router
from app.auth.validators import AuthHandler as auth_handler

app = FastAPI(title="ClicOH API")

app.include_router(hello_router, prefix="/hello", tags=["Hello"])
app.include_router(auth_router, prefix="/users", tags=["Auth"])
app.include_router(
    products_router,
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(auth_handler.get_current_user)],
)
