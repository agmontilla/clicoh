from app.exceptions import ProductNotAvailable, ProductNotFound, ProductsAreDuplicated
from app.orders.models import Order, OrderDetails
from app.orders.schemas import OrderDetailsCollection, OrderOut
from app.products.models import Product
from sqlalchemy.orm import Session


def validate_duplicate_product_id(order_details: OrderDetailsCollection) -> None:
    """
    Validates if the items are duplicated.
    """
    product_ids = [item.product_id for item in order_details.items]
    if len(product_ids) != len(set(product_ids)):
        raise ProductsAreDuplicated()


def products_are_available(
    order_details: OrderDetailsCollection, database: Session
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
    order_details: OrderDetailsCollection, database: Session
) -> OrderOut:
    """
    Creates an order.
    """
    new_order = Order()

    database.add(new_order)
    database.commit()
    database.refresh(new_order)

    for item in order_details.items:
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
