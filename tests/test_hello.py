from http import HTTPStatus
from fastapi.testclient import TestClient


class TestHello:

    ENDPOINT = "/hello"

    def test_hello_endpoint_is_ok(self, client: TestClient) -> None:

        response = client.get(self.ENDPOINT)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == "Hello World"

    def test_hello_endpoint_but_protected(
        self, client: TestClient, dummy_bearer_token: str
    ) -> None:
        response = client.get(
            self.ENDPOINT + "/user",
            headers={"Authorization": dummy_bearer_token},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == "Hello user, but protected"
