from abc import ABC, abstractmethod


class LLMQueueService(ABC):
    @abstractmethod
    async def add(self, session_id: str, user_message: str) -> str:
        pass
