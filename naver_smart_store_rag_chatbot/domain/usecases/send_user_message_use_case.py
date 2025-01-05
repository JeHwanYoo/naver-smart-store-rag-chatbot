from naver_smart_store_rag_chatbot.domain.interfaces.repositories.chat_repository import ChatRepository


class SendUserMessageUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    async def execute(self, session_id: str, user_message: str):
        chats = await self.chat_repository.find_by_session_id(session_id)

        if len(chats) > 0:
            pass
        else:
            return None
