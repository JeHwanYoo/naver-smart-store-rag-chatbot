import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from .main import app


@pytest.fixture(scope='module')
def http_client():
    return TestClient(app)


@pytest.fixture(scope='module')
def motor_client():
    return AsyncIOMotorClient('mongodb://localhost:27017')


def test_root(http_client: TestClient):
    response = http_client.get('/v1')
    assert response.status_code == 200
    assert response.text == '"OK"'


@pytest.mark.asyncio
async def test_motor(motor_client: AsyncIOMotorClient):
    ping = await motor_client.admin.command('ping')
    assert ping['ok'] == 1.0
