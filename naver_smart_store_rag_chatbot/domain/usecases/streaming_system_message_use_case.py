from naver_smart_store_rag_chatbot.domain.interfaces.repositories.chat_repository import ChatRepository
from naver_smart_store_rag_chatbot.domain.interfaces.services.llm_queue_service import LLMQueueService
from naver_smart_store_rag_chatbot.domain.interfaces.services.llm_rag_service import LLMRagService
from naver_smart_store_rag_chatbot.domain.interfaces.services.vector_db_service import VectorDBService


class StreamingSystemMessageUseCase:
    def __init__(
        self,
        chat_repository: ChatRepository,
        llm_queue_service: LLMQueueService,
        vector_db_service: VectorDBService,
        llm_rag_service: LLMRagService,
    ):
        self.chat_repository = chat_repository
        self.llm_queue_service = llm_queue_service
        self.vector_db_service = vector_db_service
        self.llm_rag_service = llm_rag_service

    async def execute(self, streaming_id: str):
        task = self.llm_queue_service.get(streaming_id)

        if not task:
            return

        session_id, user_message = task

        related_documents = await self.vector_db_service.find_related_documents(user_message=user_message)
        recent_chats = await self.chat_repository.find_recent_chats(session_id)

        system_message = ''
        for chunk in self.llm_rag_service.send_question(
            user_message,
            related_documents=related_documents,
            recent_chats=recent_chats,
        ):
            content = chunk.choices[0].delta.content
            if content:
                system_message += content
                yield content

        await self.chat_repository.save(session_id, user_message=user_message, system_message=system_message)
