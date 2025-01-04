import os

from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = AsyncIOMotorClient(os.getenv('MONGO_CONNECTION_STRING', 'mongodb://root:example@localhost:27017/'))
mongo_main_db = mongo_client.get_database(os.getenv('MONGO_MAIN_DB', 'test_db'))
