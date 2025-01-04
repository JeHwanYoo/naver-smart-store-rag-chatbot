from naver_smart_store_rag_chatbot.domain.interfaces.chat_repository import ChatRepository


class FindAllChatSessionsUseCase:
    def __init__(self, chat_session_repository: ChatRepository):
        self.chat_session_repository = chat_session_repository

    def execute(self):
        return self.chat_session_repository.find_all()
