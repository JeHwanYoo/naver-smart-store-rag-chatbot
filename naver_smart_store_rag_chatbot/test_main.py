import uuid
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
                    'user_message': f'fake user message: {i}',
                    'system_message': f'fake system message: {i}',
                    'recommends': ['fake recommends'],
                }
            )
        base_time += timedelta(minutes=3)

    await coll.insert_many(chat_histories)

    return chat_histories


@pytest_asyncio.fixture(scope='function')
async def dummy_sessions(motor_client: AsyncIOMotorClient):
    await create_dummy_chat_histories(motor_client)
    test_db = motor_client.get_database('test_db')
    coll = test_db.get_collection('chat_histories')
    return await coll.aggregate(
        [
            {
                '$group': {
                    '_id': '$session_id',
                    'created_at': {'$max': '$created_at'},
                    'first_message': {'$first': '$user_message'},
                }
            },
            {'$sort': {'created_at': -1}},
            {
                '$project': {
                    '_id': 0,
                    'session_id': '$_id',
                    'first_message': '$first_message',
                }
            },
        ]
    ).to_list(length=None)


@pytest_asyncio.fixture(scope='function')
async def dummy_chats_in_session(motor_client: AsyncIOMotorClient):
    chat_histories = await create_dummy_chat_histories(motor_client)
    session_id = chat_histories[0]['session_id']

    results = [history for history in chat_histories if history['session_id'] == session_id]
    results.sort(key=lambda x: x['created_at'])

    return [
        {'session_id': r['session_id'], 'user_message': r['user_message'], 'system_message': r['system_message']}
        for r in results
    ]


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


@pytest.mark.asyncio
async def test_get_chats_by_session_id(
    http_client: TestClient, motor_client: AsyncIOMotorClient, dummy_chats_in_session
):
    session_id = dummy_chats_in_session[0]['session_id']
    response = http_client.get(f'/v1/sessions/{session_id}/chats')

    assert response.status_code == 200
