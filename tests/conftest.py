from typing import Iterator

import pytest
from app.auth import models, schemas
from app.auth.validators import AuthHandler as auth_handler
from app.products.models import Product
from app.products.schemas import ProductOut
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
def dummy_product_id() -> str:
    fake = Faker()
    database = next(override_get_db())
    new_product = Product(name=fake.company(), price=1.0, stock=1)
    database.add(new_product)
    database.commit()

    return ProductOut.from_orm(new_product).id
