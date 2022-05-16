from typing import Iterator
import pytest
from fastapi.testclient import TestClient
from app.products.schemas import ProductIn
from http import HTTPStatus


class TestProductSchemas:
    def test_product_price_is_invalid_when_is_0(self) -> None:

        with pytest.raises(ValueError, match="Price must be greater than 0"):
            ProductIn(name="Test", price=0.0, stock=0)

    def test_product_stock_is_invalid_when_is_negative(self) -> None:

        with pytest.raises(ValueError, match="Stock cannot be negative"):
            ProductIn(name="Test", price=1.0, stock=-1)


class TestProductEndpoints:

    ENDPOINT = "/products/"

    def test_create_product_is_working(
        self, client: TestClient, dummy_bearer_token: str
    ) -> None:

        response = client.post(
            self.ENDPOINT,
            json={
                "name": "Test",
                "price": 1.0,
                "stock": 1,
            },
            headers={"Authorization": dummy_bearer_token},
        )

        assert response.status_code == HTTPStatus.CREATED

    def test_delete_a_product_is_working(
        self, client: TestClient, dummy_bearer_token: str, dummy_product_id: str
    ) -> None:

        response = client.delete(
            self.ENDPOINT + dummy_product_id,
            headers={"Authorization": dummy_bearer_token},
        )

        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_delele_a_product_that_does_not_exist(
        self, client: TestClient, dummy_bearer_token: str
    ) -> None:

        response = client.delete(
            self.ENDPOINT + "123",
            headers={"Authorization": dummy_bearer_token},
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == "Product not found"

    def test_get_a_product_is_working(
        self, client: TestClient, dummy_bearer_token: str, dummy_product_id: str
    ) -> None:

        response = client.get(
            self.ENDPOINT + dummy_product_id,
            headers={"Authorization": dummy_bearer_token},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json()["id"] == dummy_product_id

    def test_get_all_products_is_working(
        self,
        client: TestClient,
        dummy_bearer_token: str,
        dummy_insert_two_products: Iterator,
    ) -> None:

        response = client.get(
            self.ENDPOINT,
            headers={"Authorization": dummy_bearer_token},
        )

        assert response.status_code == HTTPStatus.OK
        assert len(response.json()["products"]) == 2

    def test_update_a_product_is_working(
        self,
        client: TestClient,
        dummy_bearer_token: str,
        dummy_product_id: str,
    ) -> None:

        new_values_of_product = ProductIn(name="Test", price=1.0, stock=1)
        token = dummy_bearer_token

        put_response = client.put(
            self.ENDPOINT + dummy_product_id,
            json=new_values_of_product.dict(),
            headers={"Authorization": token},
        )

        get_response = client.get(
            self.ENDPOINT + dummy_product_id, headers={"Authorization": token}
        )

        assert put_response.status_code == HTTPStatus.NO_CONTENT
        for key, value in new_values_of_product.dict().items():
            assert get_response.json()[key] == value
