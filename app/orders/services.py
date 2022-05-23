from typing import Any, Callable, Dict, Optional

import requests
from app.constants import USD_API_URL, Actions, CurrentExchanges
from app.exceptions import (
    OrderNotFound,
    ProductNotAvailable,
    ProductNotFound,
    ProductsAreDuplicated,
    USDRateNotFound,
)
from app.orders.models import Order, OrderDetails
from app.orders.schemas import (
    OrderCollectionOut,
    OrderDetailsCollectionIn,
    OrderDetailsOut,
    OrderOut,
    OrderWithDetailsOut,
    TotalBillingOut,
)
from app.products.models import Product
from sqlalchemy.orm import Session


def validate_duplicate_product_id(order_details: OrderDetailsCollectionIn) -> None:
    """
    Validates if the items are duplicated.
    """
    product_ids = [item.product_id for item in order_details.items]
    if len(product_ids) != len(set(product_ids)):
        raise ProductsAreDuplicated()


def products_are_available_when_order_is_created(
    order_details: OrderDetailsCollectionIn, database: Session
) -> None:
    """
    Validates if the products are available.
    """

    for item in order_details.items:
        product = database.query(Product).get(item.product_id)
        if product is None:
            raise ProductNotFound(item.product_id)
        if product.stock < item.quantity:
            raise ProductNotAvailable(item.product_id)


def products_are_available_when_order_is_updated(
    order_id: int, order_details: OrderDetailsCollectionIn, database: Session
) -> None:
    """
    Validates if the products are available.
    """

    order = database.query(Order).get(order_id)

    if order is None:
        raise OrderNotFound(order_id)

    current_products = {item.product_id: item.quantity for item in order.order_details}

    for item in order_details.items:
        product = database.query(Product).get(item.product_id)
        if product is None:
            raise ProductNotFound(item.product_id)

        if product.id in current_products.keys():
            if (product.stock + current_products[product.id]) - item.quantity < 0:
                raise ProductNotAvailable(item.product_id)
        else:
            if product.stock < item.quantity:
                raise ProductNotAvailable(item.product_id)


def products_are_available(action: Actions, **kwargs: Any) -> None:
    product_available: Dict[Actions, Callable] = {
        Actions.CREATE: products_are_available_when_order_is_created,
        Actions.UPDATE: products_are_available_when_order_is_updated,
    }
    product_available[action](**kwargs)


def create_new_order(
    order_details: OrderDetailsCollectionIn, database: Session
) -> OrderOut:
    """
    Creates an order.
    """
    new_order = Order()

    database.add(new_order)
    database.commit()
    database.refresh(new_order)

    for item in order_details.items:
        # TODO: Verify if I can use foreign key "product" to avoid this query.
        product = database.query(Product).get(item.product_id)
        product.stock -= item.quantity
        database.add(product)

        new_order_details = OrderDetails(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        database.add(new_order_details)

    database.commit()

    return OrderOut.from_orm(new_order)


def get_all_orders(database: Session) -> OrderCollectionOut:
    """
    Gets all orders.
    """
    orders = database.query(Order).all()
    return OrderCollectionOut(items=orders)


def get_an_order(order_id: int, database: Session) -> OrderWithDetailsOut:
    """
    Gets an order.
    """
    order = database.query(Order).get(order_id)
    if order is None:
        raise OrderNotFound(order_id)

    order_details = [
        OrderDetailsOut(product_id=item.product_id, quantity=item.quantity)
        for item in order.order_details
    ]

    return OrderWithDetailsOut(
        id=order.id, datetime=order.datetime, items=order_details
    )


def delete_an_order(order_id: int, database: Session) -> None:
    """
    Deletes an order.
    """
    order = database.query(Order).get(order_id)
    if order is None:
        raise OrderNotFound(order_id)

    for item in order.order_details:
        product = database.query(Product).get(item.product_id)
        product.stock += item.quantity
        database.add(product)

    for item in order.order_details:
        database.delete(item)

    database.delete(order)
    database.commit()


def update_an_order(
    order_id: int, order_details: OrderDetailsCollectionIn, database: Session
) -> None:
    """
    Updates an order.
    """
    order = database.query(Order).get(order_id)
    if order is None:
        raise OrderNotFound(order_id)

    for item in order.order_details:
        product = database.query(Product).get(item.product_id)
        product.stock += item.quantity
        database.add(product)

    for item in order.order_details:
        database.delete(item)

    for item in order_details.items:
        product = database.query(Product).get(item.product_id)
        product.stock -= item.quantity
        database.add(product)

    for item in order_details.items:
        new_order_details = OrderDetails(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        database.add(new_order_details)

    database.commit()


def get_total_billing(
    order_id: int, currency_exchange: CurrentExchanges, database: Session
) -> TotalBillingOut:
    """
    Gets the total billing.
    """
    order = database.query(Order).get(order_id)
    if order is None:
        raise OrderNotFound(order_id)

    f = {
        CurrentExchanges.ARS: order.get_total,
        CurrentExchanges.USD: order.get_total_usd,
    }

    return TotalBillingOut(total_billing=f[currency_exchange]())


# def get_total_billing_in_usd(order_id: int, database: Session) -> TotalBillingOut:
#     """
#     Gets the total billing in USD.
#     """
#     order = database.query(Order).get(order_id)
#     if order is None:
#         raise OrderNotFound(order_id)

#     return TotalBillingOut(total_billing=order.get_total() / get_usd_rate())


# def get_usd_rate(mode: str = "Dolar Blue") -> float:
#     """
#     Gets the USD rate.
#     """
#     response = requests.get(USD_API_URL)
#     response.raise_for_status()
#     data = response.json()

#     rate: float = 0

#     for item in data:
#         if item["casa"]["nombre"] == mode:
#             rate = float(str.replace(item["casa"]["venta"], ",", "."))
#             break
#     else:
#         raise USDRateNotFound(mode)

#     return rate
