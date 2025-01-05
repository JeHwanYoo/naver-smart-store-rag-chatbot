from abc import ABC, abstractmethod
from typing import List, Generator

from naver_smart_store_rag_chatbot.domain.entities.chat import Chat
from naver_smart_store_rag_chatbot.domain.entities.document import Document


class LLMRagService(ABC):
    @abstractmethod
    def send_question(
        self, user_message: str, related_documents: List[Document], recent_chats: List[Chat]
    ) -> Generator:
        pass
