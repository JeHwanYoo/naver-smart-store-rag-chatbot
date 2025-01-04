from fastapi import APIRouter

sessions_router = APIRouter(prefix='/sessions')


@sessions_router.get('/', description='모든 세션 목록을 불러옵니다.')
async def get_sessions():
    pass
