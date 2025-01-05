from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse

from naver_smart_store_rag_chatbot.domain.usecases.streaming_system_message_use_case import (
    StreamingSystemMessageUseCase,
)
from naver_smart_store_rag_chatbot.infrastructure.di_container import Container

streaming_router = APIRouter(prefix='/streaming')


@streaming_router.get(
    '/{streaming_id}', description='특정 스트리밍 id를 이용하여 답변에 대한 스트리밍을 받습니다 (SSE)'
)
@inject
async def stream_system_message(
    request: Request,
    streaming_id: str,
    streaming_system_message_use_case: StreamingSystemMessageUseCase = Depends(
        Provide[Container.streaming_system_message_use_case]
    ),
):
    async def event_generator():
        async for chunk in streaming_system_message_use_case.execute(streaming_id):
            if await request.is_disconnected():
                break
            yield f'data: {chunk}\n\n'

    return StreamingResponse(
        event_generator(), media_type='text/event-stream', headers={'Content-Type': 'text/event-stream; charset=utf-8'}
    )
