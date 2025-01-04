import uuid
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from naver_smart_store_rag_chatbot.api.v1.sessions.chats_response import ChatResponse
from naver_smart_store_rag_chatbot.api.v1.sessions.recommend_response import RecommendsResponse
from naver_smart_store_rag_chatbot.api.v1.sessions.send_user_message_request import SendUserMessageRequest
from naver_smart_store_rag_chatbot.api.v1.sessions.send_user_message_response import SendUserMessageResponse
from naver_smart_store_rag_chatbot.api.v1.sessions.sessions_response import SessionResponse
from naver_smart_store_rag_chatbot.infrastructure.di_container import Container

sessions_router = APIRouter(prefix='/sessions')


@sessions_router.post(
    '/{session_id}/chats', description='특정 세션에 유저 메세지를 보냅니다. 스트리밍 ID를 반환 받습니다.'
)
async def send_user_message(session_id: str, _: SendUserMessageRequest) -> SendUserMessageResponse:
    return SendUserMessageResponse(session_id=session_id, streaming_id=str(uuid.uuid4()))


@sessions_router.get('/{session_id}/chats', description='특정 세션의 대화 목록을 불러옵니다.')
async def get_chats_by_session_id(session_id: str) -> List[ChatResponse]:
    return [ChatResponse(session_id=session_id, user_message='fake question', system_message='fake answer')]


@sessions_router.get('/{session_id}/recommends', description='가장 최근 대화의 추천 질문 목록을 받습니다. (3개)')
async def get_recommends_by_session_id(session_id: str) -> RecommendsResponse:
    return RecommendsResponse(session_id=session_id, chatbot_recommends=['fake1', 'fake2', 'fake3'])


@sessions_router.get('/', description='모든 세션 목록을 불러옵니다.')
@inject
async def get_sessions(
    find_all_chat_sessions_use_case=Depends(Provide[Container.find_all_chat_sessions_use_case]),
) -> List[SessionResponse]:
    return await find_all_chat_sessions_use_case.execute()
