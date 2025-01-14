import asyncio
from typing import Optional, Tuple
from uuid import uuid4

from cachetools import TTLCache

from naver_smart_store_rag_chatbot.domain.interfaces.services.llm_queue_service import LLMQueueService


class CachetoolsLLMQueueService(LLMQueueService):
    def __init__(self, maxsize: int = 1024, ttl: int = 60):
        self.cache = TTLCache(maxsize, ttl=ttl)
        self.lock = asyncio.Lock()

    async def add(self, session_id: str, user_message: str) -> str:
        streaming_id = uuid4()
        async with self.lock:
            self.cache[str(streaming_id)] = (session_id, user_message)
        return str(streaming_id)

    async def get(self, streaming_id: str) -> Optional[Tuple[str, str]]:
        async with self.lock:
            if self.cache.get(streaming_id) is None:
                return None
            return self.cache.pop(streaming_id)
