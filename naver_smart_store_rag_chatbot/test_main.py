import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from .main import app


@pytest.fixture(scope='module')
def http_client():
    return TestClient(app)


@pytest.fixture(scope='module')
def motor_client():
    return AsyncIOMotorClient('mongodb://root:example@localhost:27017/')


async def create_dummy_sessions(motor_client: AsyncIOMotorClient):
    test_db = motor_client.get_database('test_db')
    coll = test_db.get_collection('chat_histories')
    chat_history_session_ids = [
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        str(uuid.uuid4()),
    ]

    chat_histories = []
    for session_id in chat_history_session_ids:
        for i in range(3):
            chat_histories.append(
                {
                    'session_id': session_id,
                    'created_at': datetime.now(),
                    'user_message': 'fake user message',
                    'system_message': 'fake system message',
                    'recommends': ['fake recommends'],
                }
            )

    await coll.insert_many(chat_histories)

    return [{'session_id': session_id, 'first_message': 'fake user message'} for session_id in chat_history_session_ids]


async def clear_test_db(motor_client: AsyncIOMotorClient):
    await motor_client.drop_database('test_db')


def test_root(http_client: TestClient):
    response = http_client.get('/v1')
    assert response.status_code == 200
    assert response.text == '"OK"'


@pytest.mark.asyncio
async def test_motor(motor_client: AsyncIOMotorClient):
    ping = await motor_client.admin.command('ping')
    assert ping['ok'] == 1.0


@pytest.mark.asyncio
async def test_get_sessions(http_client: TestClient, motor_client: AsyncIOMotorClient):
    response = http_client.get('/v1/sessions')

    expect = await create_dummy_sessions(motor_client)

    assert response.status_code == 200
    assert response.json() == expect

    await clear_test_db(motor_client)
