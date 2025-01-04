import uuid
from typing import List

from fastapi import APIRouter

from naver_smart_store_rag_chatbot.api.v1.sessions.chats_response import ChatResponse
from naver_smart_store_rag_chatbot.api.v1.sessions.sessions_response import SessionResponse

sessions_router = APIRouter(prefix='/sessions')


@sessions_router.get('/{session_id}/chats', description='특정 세션의 대화 목록을 불러옵니다.')
async def get_chats_by_session_id(session_id: str) -> List[ChatResponse]:
    return [ChatResponse(session_id=session_id, user_message='fake question', system_message='fake answer')]


@sessions_router.get('/', description='모든 세션 목록을 불러옵니다.')
async def get_sessions() -> List[SessionResponse]:
    return [SessionResponse(session_id=str(uuid.uuid4()), first_message='fake message')]
