from http import HTTPStatus
from typing import Iterator

from app.auth.validators import AuthHandler as auth_handler
from faker import Faker
from fastapi.testclient import TestClient


class TestEndpointUsers:

    PREFIX = "/users/{}"
    SIGNUP_ENDPOINT = PREFIX.format("signup")
    LOGIN_ENDPOINT = PREFIX.format("login")

    def test_user_is_created_successfully(self, client: TestClient) -> None:
        fake = Faker()
        response = client.post(
            self.SIGNUP_ENDPOINT,
            json={"email": fake.email(), "password": fake.password()},
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == "User Created"

    def test_user_can_login_succesfully(
        self, client: TestClient, dummy_user: Iterator
    ) -> None:
        response = client.post(
            self.LOGIN_ENDPOINT,
            json={"email": "test_user@gmail.com", "password": "123456"},
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json()["access_token"].startswith("Bearer ")

    def test_user_is_already_exists(
        self, client: TestClient, dummy_user: Iterator
    ) -> None:
        response = client.post(
            self.SIGNUP_ENDPOINT,
            json={"email": "test_user@gmail.com", "password": "123456"},
        )

        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json()["detail"] == "User already exists"

    def test_user_is_not_authorize(self, client: TestClient) -> None:
        fake = Faker()
        response = client.post(
            self.LOGIN_ENDPOINT,
            json={"email": fake.email(), "password": fake.password()},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()["detail"] == "Invalid username and/or credentials"


class TestAuthHandler:
    def test_get_password_has_returns_str(self) -> None:
        assert isinstance(auth_handler.get_password_hash("123456"), str)

    def test_verify_password_returns_bool(self) -> None:
        assert isinstance(
            auth_handler.verify_password(
                "123456", auth_handler.get_password_hash("123456")
            ),
            bool,
        )

    def test_verify_password_is_working(self) -> None:
        assert auth_handler.verify_password(
            "123456", auth_handler.get_password_hash("123456")
        )
