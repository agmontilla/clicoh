from app.exceptions import (
    OrderNotFound,
    ProductNotAvailable,
    ProductNotFound,
    ProductsAreDuplicated,
)
from app.orders.models import Order, OrderDetails
from app.orders.schemas import (
    OrderCollectionOut,
    OrderDetailsCollectionIn,
    OrderOut,
    OrderWithDetailsOut,
    OrderDetailsOut,
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


def products_are_available(
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
        # TODO: Use foreign key "product" to avoid this query.
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
