import uuid
from collections import defaultdict
from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from .main import app


@pytest.fixture(scope='function')
def http_client():
    return TestClient(app)


@pytest.fixture(scope='function')
def motor_client():
    return AsyncIOMotorClient('mongodb://root:example@localhost:27017/')


async def create_dummy_chat_histories(motor_client: AsyncIOMotorClient):
    test_db = motor_client.get_database('test_db')
    coll = test_db.get_collection('chat_histories')
    chat_history_session_ids = [
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        str(uuid.uuid4()),
    ]

    chat_histories = []
    base_time = datetime.now()

    for session_id in chat_history_session_ids:
        for i in range(3):
            chat_histories.append(
                {
                    'session_id': session_id,
                    'created_at': base_time + timedelta(minutes=i),
                    'user_message': 'fake user message',
                    'system_message': 'fake system message',
                    'recommends': ['fake recommends'],
                }
            )
        base_time += timedelta(minutes=3)

    await coll.insert_many(chat_histories)

    return chat_histories


@pytest_asyncio.fixture(scope='function')
async def dummy_sessions(motor_client: AsyncIOMotorClient):
    chat_histories = await create_dummy_chat_histories(motor_client)
    grouped = defaultdict(list)

    for history in chat_histories:
        grouped[history['session_id']].append(history)

    results = []
    for session_id, histories in grouped.items():
        sorted_histories = sorted(histories, key=lambda x: x['created_at'], reverse=True)
        first_message = sorted_histories[-1]['user_message']
        latest_created_at = sorted_histories[0]['created_at']

        results.append({'session_id': session_id, 'created_at': latest_created_at, 'first_message': first_message})

    results.sort(key=lambda x: x['created_at'], reverse=True)

    return [{'session_id': r['session_id'], 'first_message': 'fake user message'} for r in results]


async def clear_test_db(motor_client: AsyncIOMotorClient):
    await motor_client.drop_database('test_db')


@pytest_asyncio.fixture(autouse=True)
async def clean_test_db(motor_client: AsyncIOMotorClient):
    yield
    await clear_test_db(motor_client)


def test_root(http_client: TestClient):
    response = http_client.get('/v1')
    assert response.status_code == 200
    assert response.text == '"OK"'


@pytest.mark.asyncio
async def test_motor(motor_client: AsyncIOMotorClient):
    ping = await motor_client.admin.command('ping')
    assert ping['ok'] == 1.0


@pytest.mark.asyncio
async def test_get_sessions(http_client: TestClient, motor_client: AsyncIOMotorClient, dummy_sessions):
    response = http_client.get('/v1/sessions')

    assert response.status_code == 200
    assert response.json() == dummy_sessions
