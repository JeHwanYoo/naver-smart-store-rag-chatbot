from naver_smart_store_rag_chatbot.domain.interfaces.services.llm_queue_service import LLMQueueService


class SendUserMessageUseCase:
    def __init__(self, llm_queue_service: LLMQueueService):
        self.llm_queue_service = llm_queue_service

    async def execute(self, session_id: str, user_message: str):
        return await self.llm_queue_service.add(session_id, user_message)
