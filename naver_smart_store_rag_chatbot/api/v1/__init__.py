from fastapi import APIRouter

# APIRouter 생성 및 v1 경로 설정
v1_router = APIRouter(prefix='/v1')


@v1_router.get('/')
async def root():
    """
    Health Check For V1
    :return:
    """
    return 'OK'
