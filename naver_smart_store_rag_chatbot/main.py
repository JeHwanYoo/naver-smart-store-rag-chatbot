from fastapi import FastAPI

from naver_smart_store_rag_chatbot.api.v1 import v1_router
from naver_smart_store_rag_chatbot.infrastructure.di_container import Container
from naver_smart_store_rag_chatbot.infrastructure.repositories.mongo_chat_repository import MongoChatRepository
from naver_smart_store_rag_chatbot.infrastructure.repositories.mongo_chat_session_repository import (
    MongoChatSessionRepository,
)

app = FastAPI()

app.include_router(v1_router)

# DI
container = Container(chat_session_repository=MongoChatSessionRepository(), chat_repository=MongoChatRepository())
container.wire(
    modules=[
        'naver_smart_store_rag_chatbot.api.v1.sessions',
    ]
)
