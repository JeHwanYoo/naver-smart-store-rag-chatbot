from fastapi import FastAPI

from naver_smart_store_rag_chatbot.api.v1 import v1_router

app = FastAPI()

app.include_router(v1_router)
