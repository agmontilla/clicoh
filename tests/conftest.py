from typing import Callable, Iterator

import pytest
from app.auth import models, schemas
from app.auth.validators import AuthHandler as auth_handler
from app.products.models import Product
from app.products.schemas import ProductOut
from app.orders.models import Order, OrderDetails
from faker import Faker
from fastapi.testclient import TestClient

from .conf_test_database import app, override_get_db


@pytest.fixture()
def client() -> TestClient:
    """App fixture."""
    # app = create_app() # TODO: create_app()
    return TestClient(app)


@pytest.fixture()
def dummy_user() -> Iterator:
    database = next(override_get_db())
    new_user = models.User(email="test_user@gmail.com", password="123456")
    database.add(new_user)
    database.commit()

    yield

    database.delete(new_user)
    database.commit()


@pytest.fixture()
def dummy_bearer_token() -> str:
    """Dummy bearer token."""
    fake = Faker()
    fake_user = schemas.User(email=fake.email(), password=fake.password())
    return "Bearer " + auth_handler.encode_token(fake_user.dict())


@pytest.fixture()
def dummy_insert_two_products() -> Iterator:
    fake = Faker()
    database = next(override_get_db())
    database.query(Product).delete()

    database.add_all(
        [
            Product(name=fake.company(), price=1.0, stock=1),
            Product(name=fake.company(), price=1.0, stock=1),
        ]
    )
    database.commit()

    yield

    database.query(Product).delete()
    database.commit()


@pytest.fixture()
def dummy_product_id() -> Callable[[float, int], str]:
    def create_dummy_product_id(price: float = 1.0, stock: int = 1) -> str:
        fake = Faker()
        database = next(override_get_db())
        new_product = Product(name=fake.company(), price=price, stock=stock)
        database.add(new_product)
        database.commit()

        return ProductOut.from_orm(new_product).id

    return create_dummy_product_id


@pytest.fixture()
def delete_all_orders() -> Iterator:
    database = next(override_get_db())
    database.query(Order).delete()
    database.query(OrderDetails).delete()
    database.commit()

    yield

    database.query(Order).delete()
    database.query(OrderDetails).delete()
    database.commit()
