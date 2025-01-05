from naver_smart_store_rag_chatbot.domain.interfaces.repositories.chat_repository import ChatRepository
from naver_smart_store_rag_chatbot.domain.interfaces.services.llm_queue_service import LLMQueueService


class StreamingSystemMessageUseCase:
    def __init__(
        self, chat_repository: ChatRepository, llm_queue_service: LLMQueueService, vector_db_service, llm_rag_service
    ):
        self.chat_repository = chat_repository
        self.llm_queue_service = llm_queue_service
        self.vector_db_service = vector_db_service
        self.llm_rag_service = llm_rag_service
