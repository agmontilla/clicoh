import pytest
from app import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """App fixture."""
    # app = create_app()
    return TestClient(app)
