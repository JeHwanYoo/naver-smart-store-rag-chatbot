from naver_smart_store_rag_chatbot.domain.interfaces.repositories.chat_session_repository import ChatSessionRepository


class FindAllChatSessionsUseCase:
    def __init__(self, chat_session_repository: ChatSessionRepository):
        self.chat_session_repository = chat_session_repository

    def execute(self):
        return self.chat_session_repository.find_all()
