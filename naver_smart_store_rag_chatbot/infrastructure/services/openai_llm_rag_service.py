import os
from typing import List, Generator

import openai

from naver_smart_store_rag_chatbot.domain.entities.chat import Chat
from naver_smart_store_rag_chatbot.domain.entities.document import Document
from naver_smart_store_rag_chatbot.domain.interfaces.services.llm_rag_service import LLMRagService


class OpenAILLMRagService(LLMRagService):
    def send_question(
        self, user_message: str, related_documents: List[Document], recent_chats: List[Chat]
    ) -> Generator:
        client = openai.OpenAI(
            api_key=os.getenv('OPEN_AI_KEY'),
        )
        messages = [
            {
                'role': 'system',
                'content': """
You are an expert in Naver Smart Store. Your task is to read the provided FAQ documents and answer user queries based on them. When answering, you must strictly adhere to the following rules:

Rules:
	1. You must base your answers on the provided FAQ documents. If no relevant documents are provided, the documents are inappropriate, do not answer.
	2. Consider the user’s previous questions and context to provide a more suitable answer.
	3. After answering the user’s question, you must generate additional related questions that the user might be curious about within the context of the Q&A. Use Related Titles to generate these questions. Provide at least two additional related questions.
    4. Format your output as simple HTML.
    5. Respond in Korean.
    6.If the question is unrelated to Naver Smart Store:
      - Respond with: “저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다.”
	  - Additionally, generate a related question to guide the user back to Smart Store topics.

Example:
    Related Question Example:
    ```
    User: 미성년자도 판매 회원 등록이 가능한가요?
    Chatbot:
    <p>네이버 스마트스토어는 만 14세 미만의 개인(개인 사업자 포함) 또는 법인사업자는 입점이 불가함을 양해 부탁 드립니다.</p>
    <ul>
        <li>등록에 필요한 서류 안내해드릴까요?</li>
        <li>등록 절차는 얼마나 오래 걸리는지 안내가 필요하신가요?</li>
    </ul>
    ```

    Unrelated Question Example:
    ```
    User: 오늘 저녁에 여의도 가려는데 맛집 추천좀 해줄래?
    <p>저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다.</p>
    <ul>
        <li>음식도 스토어 등록이 가능한지 궁금하신가요?</li>
    </ul>
    ```
""",
            },
            {
                'role': 'user',
                'content': f"""
FAQ Documents: {'\n\n'.join([f'질문:{doc.title} \n답변: {doc.content}' for doc in related_documents])}
Previous Questions and Context: {'\n\n'.join([f'사용자 질문: {chat.user_message}\n챗봇 답변: {chat.system_message}' for chat in recent_chats])}
Related Titles: {', '.join([', '.join(doc.related_titles) for doc in related_documents])}

User Question: {user_message}
""",
            },
        ]

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            temperature=0.7,
            stream=True,
        )

        for chunk in response:
            content = chunk.choices[0].delta.content
            yield content
