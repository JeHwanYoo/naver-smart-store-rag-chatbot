from abc import ABC, abstractmethod
from typing import Optional, Tuple


class LLMQueueService(ABC):
    @abstractmethod
    async def add(self, session_id: str, user_message: str) -> str:
        pass

    @abstractmethod
    async def get(self, streaming_id: str) -> Optional[Tuple[str, str]]:
        pass
