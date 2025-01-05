from abc import ABC, abstractmethod
from typing import List

from naver_smart_store_rag_chatbot.domain.entities.chat_session import ChatSession


class ChatSessionRepository(ABC):
    @abstractmethod
    async def find_all(self) -> List[ChatSession]:
        pass
