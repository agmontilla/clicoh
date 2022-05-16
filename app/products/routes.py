from http import HTTPStatus

from app.database import get_db
from app.products import schemas
from app.products.services import (
    create_new_product,
    delete_existing_product,
    get_all_products,
    get_existing_product,
    update_a_product,
)
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

products_router = APIRouter()


@products_router.post(
    "/", response_model=schemas.ProductOut, status_code=HTTPStatus.CREATED
)
def create_product(
    product: schemas.ProductIn, database: Session = Depends(get_db)
) -> schemas.ProductOut:
    return create_new_product(product, database)


@products_router.delete(
    "/{product_id}",
    status_code=HTTPStatus.NO_CONTENT,
    responses={HTTPStatus.NOT_FOUND.value: {"detail": "Product not found"}},
)
def remove_product(product_id: str, database: Session = Depends(get_db)) -> None:
    try:
        delete_existing_product(product_id, database)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Product not found"
        )

    return


@products_router.get(
    "/{product_id}",
    response_model=schemas.ProductOut,
    responses={HTTPStatus.NOT_FOUND.value: {"detail": "Product not found"}},
)
def get_product(
    product_id: str, database: Session = Depends(get_db)
) -> schemas.ProductOut:
    try:
        product = get_existing_product(product_id, database)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Product not found"
        )

    return product


@products_router.get("/", response_model=schemas.ProductsOutCollection)
def get_products(database: Session = Depends(get_db)) -> schemas.ProductsOutCollection:
    return get_all_products(database)


@products_router.put(
    "/{product_id}",
    status_code=HTTPStatus.NO_CONTENT,
    responses={HTTPStatus.NOT_FOUND.value: {"detail": "Product not found"}},
)
def update_product(
    product_id: str, product: schemas.ProductIn, database: Session = Depends(get_db)
) -> None:

    try:
        update_a_product(product_id, product, database)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Product not found"
        )

    return
