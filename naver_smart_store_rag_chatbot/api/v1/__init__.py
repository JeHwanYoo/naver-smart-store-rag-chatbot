from fastapi import APIRouter

from naver_smart_store_rag_chatbot.api.v1.sessions import sessions_router
from naver_smart_store_rag_chatbot.api.v1.streaming import streaming_router

# APIRouter 생성 및 v1 경로 설정
v1_router = APIRouter(prefix='/v1')
v1_router.include_router(sessions_router)
v1_router.include_router(streaming_router)


@v1_router.get('/')
async def root():
    """
    Health Check For V1
    :return:
    """
    return 'OK'
