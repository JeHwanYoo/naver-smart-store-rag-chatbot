from naver_smart_store_rag_chatbot.domain.interfaces.chat_repository import ChatRepository


class SendUserMessageUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository
