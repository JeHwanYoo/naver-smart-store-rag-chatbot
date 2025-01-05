from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from naver_smart_store_rag_chatbot.api.v1 import v1_router
from naver_smart_store_rag_chatbot.infrastructure.di_container import Container
from naver_smart_store_rag_chatbot.infrastructure.repositories.mongo_chat_repository import MongoChatRepository
from naver_smart_store_rag_chatbot.infrastructure.repositories.mongo_chat_session_repository import (
    MongoChatSessionRepository,
)
from naver_smart_store_rag_chatbot.infrastructure.services.cachetools_llm_queue_service import CachetoolsLLMQueueService
from naver_smart_store_rag_chatbot.infrastructure.services.chorma_db_vector_db_service import ChromaDBVectorDBService
from naver_smart_store_rag_chatbot.infrastructure.services.openai_llm_rag_service import OpenAILLMRagService

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
    vector_db_service=ChromaDBVectorDBService(),
    llm_rag_service=OpenAILLMRagService(),
)
container.wire(
    modules=[
        'naver_smart_store_rag_chatbot.api.v1.sessions',
    ]
)
