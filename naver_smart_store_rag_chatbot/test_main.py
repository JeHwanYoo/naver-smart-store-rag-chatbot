import pytest
from fastapi.testclient import TestClient

from .main import app


@pytest.fixture(scope='module')
def http_client():
    with TestClient(app) as http_client:
        yield http_client
        http_client.close()


def test_root(http_client: TestClient):
    response = http_client.get('/v1')
    assert response.status_code == 200
    assert response.text == '"OK"'
