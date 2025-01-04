from fastapi import APIRouter

streaming_router = APIRouter(prefix='/streaming')


@streaming_router.get(
    '/{streaming_id}', description='특정 스트리밍 id를 이용하여 답변에 대한 스트리밍을 받습니다 (SSE)'
)
async def get_streaming_by_id(_: str):
    pass
