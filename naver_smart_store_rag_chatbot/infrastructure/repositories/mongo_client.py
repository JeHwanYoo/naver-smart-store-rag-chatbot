import os
from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient


@asynccontextmanager
async def get_mongo_database():
    mongo_client = AsyncIOMotorClient(os.getenv('MONGO_CONNECTION_STRING', 'mongodb://root:example@localhost:27017/'))
    db = mongo_client.get_database(os.getenv('MONGO_MAIN_DB', 'test_db'))
    try:
        yield db
    finally:
        mongo_client.close()
