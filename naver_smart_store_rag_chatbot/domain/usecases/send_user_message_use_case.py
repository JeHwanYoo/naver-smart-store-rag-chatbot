from naver_smart_store_rag_chatbot.domain.interfaces.repositories.chat_repository import ChatRepository
from naver_smart_store_rag_chatbot.domain.interfaces.services.llm_queue_service import LLMQueueService


class SendUserMessageUseCase:
    def __init__(self, chat_repository: ChatRepository, llm_queue_service: LLMQueueService):
        self.chat_repository = chat_repository
        self.llm_queue_service = llm_queue_service

    async def execute(self, session_id: str, user_message: str):
        chats = await self.chat_repository.find_by_session_id(session_id)

        if len(chats) > 0:
            return await self.llm_queue_service.add(session_id, user_message)
        else:
            return None
