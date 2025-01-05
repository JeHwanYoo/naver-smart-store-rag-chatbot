from typing import List

from naver_smart_store_rag_chatbot.domain.entities.chat import Chat
from naver_smart_store_rag_chatbot.domain.interfaces.chat_repository import ChatRepository
from naver_smart_store_rag_chatbot.infrastructure.repositories.mongo_client import mongo_main_db

collection_name = 'chat_histories'


class MongoChatRepository(ChatRepository):
    async def find_by_session_id(self, session_id: str) -> List[Chat]:
        coll = mongo_main_db.get_collection(collection_name)
        cursor = coll.find({'session_id': session_id})
        results = await cursor.to_list(length=None)

        return [
            Chat(
                session_id=result['session_id'],
                user_message=result['user_message'],
                system_message=result['system_message'],
            )
            for result in results
        ]
