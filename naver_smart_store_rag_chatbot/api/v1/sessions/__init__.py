import uuid
from typing import List

from fastapi import APIRouter

from naver_smart_store_rag_chatbot.api.v1.sessions.sessions_response import SessionResponse

sessions_router = APIRouter(prefix='/sessions')


@sessions_router.get('/', description='모든 세션 목록을 불러옵니다.')
async def get_sessions() -> List[SessionResponse]:
    return [SessionResponse(session_id=str(uuid.uuid4()), first_message='fake message')]
