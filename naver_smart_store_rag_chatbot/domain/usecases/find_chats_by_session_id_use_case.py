from naver_smart_store_rag_chatbot.domain.interfaces.chat_repository import ChatRepository


class FindChatsBySessionIdUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    def execute(self, session_id: str):
        return self.chat_repository.find_by_session_id(session_id)
