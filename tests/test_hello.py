from http import HTTPStatus
from fastapi.testclient import TestClient


class TestHello:

    ENDPOINT = "/hello"

    def test_hello_endpoint_is_ok(self, client: TestClient) -> None:

        response = client.get(self.ENDPOINT)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == "Hello World"
