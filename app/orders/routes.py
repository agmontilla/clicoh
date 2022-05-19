from http import HTTPStatus

from app.exceptions import ProductNotAvailable, ProductNotFound, ProductsAreDuplicated
from app.orders import schemas
from app.orders.services import (
    products_are_available,
    validate_duplicate_product_id,
    create_new_order,
)
from app.database import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

orders_router = APIRouter()


# @orders_router.get("/", response_model=schemas.OrdersOutCollection)
# def get_orders(database: Session = Depends(get_db)) -> schemas.OrdersOutCollection:
#     return get_all_orders(database)


@orders_router.post(
    "/", response_model=schemas.OrderOut, status_code=HTTPStatus.CREATED
)
def create_order(
    order_details: schemas.OrderDetailsCollection, database: Session = Depends(get_db)
) -> schemas.OrderOut:

    try:
        validate_duplicate_product_id(order_details)
        products_are_available(order_details, database)
        new_order = create_new_order(order_details, database)

    except ProductNotFound as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except ProductNotAvailable as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except ProductsAreDuplicated:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Duplicate product id."
        )

    return new_order
