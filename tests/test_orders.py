from http import HTTPStatus
from typing import Callable, Iterator

import pytest
from fastapi.testclient import TestClient


class TestOrdersEndpoints:

    ENDPOINT = "/orders/"
    TOTAL_BILLING = "/orders/{}/billing"

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

    def test_get_all_orders_is_working(
        self,
        client: TestClient,
        dummy_bearer_token: str,
        dummy_product_id: Callable[[float, int], str],
        delete_all_orders: Iterator,
    ) -> None:

        product_id = dummy_product_id(1.0, 2)

        response = client.post(
            self.ENDPOINT,
            json={"items": [{"product_id": product_id, "quantity": 1}]},
            headers={"Authorization": dummy_bearer_token},
        )

        response = client.get(
            self.ENDPOINT, headers={"Authorization": dummy_bearer_token}
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json()["items"][0]["id"] == 1

    def test_get_an_order_is_working(
        self,
        client: TestClient,
        dummy_bearer_token: str,
        dummy_product_id: Callable[[float, int], str],
        delete_all_orders: Iterator,
    ) -> None:

        product_id = dummy_product_id(1.0, 2)

        response = client.post(
            self.ENDPOINT,
            json={"items": [{"product_id": product_id, "quantity": 1}]},
            headers={"Authorization": dummy_bearer_token},
        )

        response = client.get(
            self.ENDPOINT + "1", headers={"Authorization": dummy_bearer_token}
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json()["id"] == 1
        assert response.json()["items"][0]["product_id"] == product_id
        assert response.json()["items"][0]["quantity"] == 1
        assert len(response.json()["items"]) == 1

    def test_delete_an_order_is_working(
        self,
        client: TestClient,
        dummy_bearer_token: str,
        dummy_product_id: Callable[[float, int], str],
        delete_all_orders: Iterator,
    ) -> None:

        product_id = dummy_product_id(1.0, 2)

        response = client.post(
            self.ENDPOINT,
            json={"items": [{"product_id": product_id, "quantity": 1}]},
            headers={"Authorization": dummy_bearer_token},
        )

        response = client.delete(
            self.ENDPOINT + "1", headers={"Authorization": dummy_bearer_token}
        )

        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_update_an_order_is_working(
        self,
        client: TestClient,
        dummy_bearer_token: str,
        dummy_product_id: Callable[[float, int], str],
        delete_all_orders: Iterator,
    ) -> None:

        product_id = dummy_product_id(1.0, 3)

        response = client.post(
            self.ENDPOINT,
            json={"items": [{"product_id": product_id, "quantity": 1}]},
            headers={"Authorization": dummy_bearer_token},
        )

        response = client.put(
            self.ENDPOINT + "1",
            json={"items": [{"product_id": product_id, "quantity": 2}]},
            headers={"Authorization": dummy_bearer_token},
        )

        assert response.status_code == HTTPStatus.NO_CONTENT

    @pytest.mark.parametrize(
        "currency, result",
        [("Pesos", 6.0), ("Dolar Blue", 6 / 204.50)],
    )
    def test_get_total_billing(
        self,
        client: TestClient,
        dummy_bearer_token: str,
        dummy_product_id: Callable[[float, int], str],
        currency: str,
        result: float,
        delete_all_orders: Iterator,
        mock_usd_rate: Iterator,
    ) -> None:

        product_id1 = dummy_product_id(1.0, 3)
        product_id2 = dummy_product_id(2.0, 3)

        response = client.post(
            self.ENDPOINT,
            json={
                "items": [
                    {"product_id": product_id1, "quantity": 2},
                    {"product_id": product_id2, "quantity": 2},
                ]
            },
            headers={"Authorization": dummy_bearer_token},
        )

        response = client.get(
            self.TOTAL_BILLING.format("1"),
            headers={"Authorization": dummy_bearer_token},
            params={"currency_exchange": currency},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json()["total_billing"] == result
