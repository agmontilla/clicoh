from http import HTTPStatus
from typing import Callable

from fastapi.testclient import TestClient


class TestOrdersEndpoints:

    ENDPOINT = "/orders/"

    def test_create_an_order_is_working(
        self,
        client: TestClient,
        dummy_product_id: Callable[[float, int], str],
        dummy_bearer_token: str,
    ) -> None:

        product_id = dummy_product_id(1.0, 6)

        response = client.post(
            self.ENDPOINT,
            json={"items": [{"product_id": product_id, "quantity": 1}]},
            headers={"Authorization": dummy_bearer_token},
        )

        assert response.status_code == HTTPStatus.CREATED
        assert isinstance(response.json()["id"], int)
        assert isinstance(response.json()["datetime"], str)
