from http import HTTPStatus
from typing import Optional

from app.constants import Actions, CurrentExchanges
from app.database import get_db
from app.exceptions import (
    OrderNotFound,
    ProductNotAvailable,
    ProductNotFound,
    ProductsAreDuplicated,
)
from app.orders import schemas
from app.orders.services import (
    create_new_order,  # get_total_billing_in_usd,
    delete_an_order,
    get_all_orders,
    get_an_order,
    get_total_billing,
    products_are_available,
    update_an_order,
    validate_duplicate_product_id,
)
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

orders_router = APIRouter()

# TODO: Documenting all response codes


@orders_router.post(
    "/", response_model=schemas.OrderOut, status_code=HTTPStatus.CREATED
)
def create_order(
    order_details: schemas.OrderDetailsCollectionIn, database: Session = Depends(get_db)
) -> schemas.OrderOut:

    try:
        validate_duplicate_product_id(order_details)
        products_are_available(
            Actions.CREATE, order_details=order_details, database=database
        )
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


@orders_router.get("/", response_model=schemas.OrderCollectionOut)
def get_orders(database: Session = Depends(get_db)) -> schemas.OrderCollectionOut:
    return get_all_orders(database)


@orders_router.get("/{order_id}", response_model=schemas.OrderWithDetailsOut)
def get_order(
    order_id: int, database: Session = Depends(get_db)
) -> schemas.OrderWithDetailsOut:
    try:
        return get_an_order(order_id, database)
    except OrderNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found.")


@orders_router.delete("/{order_id}", status_code=HTTPStatus.NO_CONTENT)
def remove_order(order_id: int, database: Session = Depends(get_db)) -> None:
    try:
        delete_an_order(order_id, database)
    except OrderNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found.")


@orders_router.put("/{order_id}", status_code=HTTPStatus.NO_CONTENT)
def update_order(
    order_id: int,
    order_details: schemas.OrderDetailsCollectionIn,
    database: Session = Depends(get_db),
) -> None:

    try:
        validate_duplicate_product_id(order_details)
        products_are_available(
            Actions.UPDATE,
            order_id=order_id,
            order_details=order_details,
            database=database,
        )
        update_an_order(order_id, order_details, database)

    except (OrderNotFound, ProductNotFound) as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except ProductNotAvailable as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except ProductsAreDuplicated:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Duplicate product id."
        )


@orders_router.get("/{order_id}/billing", response_model=schemas.TotalBillingOut)
def get_order_total_billing(
    order_id: int,
    currency_exchange: CurrentExchanges,
    database: Session = Depends(get_db),
) -> schemas.TotalBillingOut:
    try:
        return get_total_billing(order_id, currency_exchange, database)
    except OrderNotFound as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
