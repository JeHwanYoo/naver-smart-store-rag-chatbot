from fastapi import FastAPI

from naver_smart_store_rag_chatbot.api.v1 import v1_router
from naver_smart_store_rag_chatbot.infrastructure.di_container import Container
from naver_smart_store_rag_chatbot.infrastructure.repositories.mongo_chat_repository import MongoChatRepository
from naver_smart_store_rag_chatbot.infrastructure.repositories.mongo_chat_session_repository import (
    MongoChatSessionRepository,
)
from naver_smart_store_rag_chatbot.infrastructure.services.cachetools_llm_queue_service import CachetoolsLLMQueueService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(v1_router)

# DI
container = Container(
    chat_session_repository=MongoChatSessionRepository(),
    chat_repository=MongoChatRepository(),
    llm_queue_service=CachetoolsLLMQueueService(),
)
container.wire(
    modules=[
        'naver_smart_store_rag_chatbot.api.v1.sessions',
    ]
)
