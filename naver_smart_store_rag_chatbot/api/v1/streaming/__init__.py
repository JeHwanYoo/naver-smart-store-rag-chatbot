from dependency_injector.wiring import Provide
from fastapi import APIRouter, Request, Depends

from naver_smart_store_rag_chatbot.domain.usecases.streaming_system_message_use_case import (
    StreamingSystemMessageUseCase,
)
from naver_smart_store_rag_chatbot.infrastructure.di_container import Container
from fastapi.responses import StreamingResponse

streaming_router = APIRouter(prefix='/streaming')


@streaming_router.post(
    '/{streaming_id}', description='특정 스트리밍 id를 이용하여 답변에 대한 스트리밍을 받습니다 (SSE)'
)
async def stream_system_message(
    request: Request,
    streaming_id: str,
    streaming_system_message_use_case: StreamingSystemMessageUseCase = Depends(
        Provide[Container.streaming_system_message_use_case]
    ),
):
    async def event_generator():
        for chunk in await streaming_system_message_use_case.execute(streaming_id):
            if await request.is_disconnected():
                break
            yield chunk

    return StreamingResponse(event_generator(), media_type='text/event-stream')
