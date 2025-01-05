from fastapi import APIRouter

streaming_router = APIRouter(prefix='/streaming')


@streaming_router.post(
    '/{streaming_id}', description='특정 스트리밍 id를 이용하여 답변에 대한 스트리밍을 받습니다 (SSE)'
)
async def stream_system_message(streaming_id: str):
    pass
