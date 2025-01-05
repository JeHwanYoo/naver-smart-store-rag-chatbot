from abc import ABC, abstractmethod
from typing import List

from naver_smart_store_rag_chatbot.domain.entities.chat import Chat


class ChatRepository(ABC):
    @abstractmethod
    async def find_by_session_id(self, session_id: str) -> List[Chat]:
        pass

    @abstractmethod
    async def find_recent_chats(self, session_id: str, limit=5) -> List[Chat]:
        pass

    @abstractmethod
    async def save(self, session_id: str, user_message: str, system_message: str) -> None:
        pass
