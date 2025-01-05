from abc import ABC, abstractmethod
from typing import List

from naver_smart_store_rag_chatbot.domain.entities.document import Document


class VectorDBService(ABC):
    @abstractmethod
    async def find_related_documents(self, user_message: str, limit=5) -> List[Document]:
        pass

    @abstractmethod
    async def save(self, session_id: str, user_message: str, system_message: str) -> None:
        pass
