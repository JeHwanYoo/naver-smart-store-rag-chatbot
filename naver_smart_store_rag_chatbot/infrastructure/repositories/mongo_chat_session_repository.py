from typing import List

from naver_smart_store_rag_chatbot.domain.entities.chat_session import ChatSession
from naver_smart_store_rag_chatbot.domain.interfaces.chat_session_repository import ChatSessionRepository
from naver_smart_store_rag_chatbot.infrastructure.repositories.mongo_client import mongo_main_db

collection_name = 'chat_sessions'


class MongoChatSessionRepository(ChatSessionRepository):
    async def find_all(self) -> List[ChatSession]:
        pipeline = [
            {
                '$group': {
                    '_id': '$session_id',
                    'created_at': {'$max': '$created_at'},
                    'first_message': {'$first': '$user_message'},
                }
            },
            {'$sort': {'created_at': -1}},
        ]

        coll = mongo_main_db.get_collection(collection_name)
        cursor = coll.aggregate(pipeline)
        results = await cursor.to_list(length=None)

        return [
            ChatSession(
                session_id=result['_id'],
                first_message=result['first_message'],
            )
            for result in results
        ]
