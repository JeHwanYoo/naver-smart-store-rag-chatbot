import uuid
from typing import List

from fastapi import APIRouter

from naver_smart_store_rag_chatbot.api.v1.sessions.chats_response import ChatResponse
from naver_smart_store_rag_chatbot.api.v1.sessions.send_user_message_request import SendUserMessageRequest
from naver_smart_store_rag_chatbot.api.v1.sessions.send_user_message_response import SendUserMessageResponse
from naver_smart_store_rag_chatbot.api.v1.sessions.sessions_response import SessionResponse

sessions_router = APIRouter(prefix='/sessions')


@sessions_router.post(
    '/{session_id}/chats', description='특정 세션에 유저 메세지를 보냅니다. 스트리밍 ID를 반환 받습니다.'
)
async def send_user_message(session_id: str, _: SendUserMessageRequest) -> SendUserMessageResponse:
    return SendUserMessageResponse(session_id=session_id, streaming_id=str(uuid.uuid4()))


@sessions_router.get('/{session_id}/chats', description='특정 세션의 대화 목록을 불러옵니다.')
async def get_chats_by_session_id(session_id: str) -> List[ChatResponse]:
    return [ChatResponse(session_id=session_id, user_message='fake question', system_message='fake answer')]


@sessions_router.get('/', description='모든 세션 목록을 불러옵니다.')
async def get_sessions() -> List[SessionResponse]:
    return [SessionResponse(session_id=str(uuid.uuid4()), first_message='fake message')]
