from dependency_injector import containers, providers

from naver_smart_store_rag_chatbot.domain.interfaces.repositories.chat_repository import ChatRepository
from naver_smart_store_rag_chatbot.domain.interfaces.repositories.chat_session_repository import ChatSessionRepository
from naver_smart_store_rag_chatbot.domain.interfaces.services.llm_queue_service import LLMQueueService
from naver_smart_store_rag_chatbot.domain.usecases.find_all_chat_sessions_use_case import FindAllChatSessionsUseCase
from naver_smart_store_rag_chatbot.domain.usecases.find_chats_by_session_id_use_case import FindChatsBySessionIdUseCase
from naver_smart_store_rag_chatbot.domain.usecases.send_user_message_use_case import SendUserMessageUseCase


class Container(containers.DeclarativeContainer):
    chat_session_repository = providers.Dependency(instance_of=ChatSessionRepository)
    chat_repository = providers.Dependency(instance_of=ChatRepository)
    llm_queue_service = providers.Dependency(instance_of=LLMQueueService)

    find_all_chat_sessions_use_case = providers.Factory(
        FindAllChatSessionsUseCase,
        chat_session_repository=chat_session_repository,
    )

    find_chats_by_session_id_use_case = providers.Factory(
        FindChatsBySessionIdUseCase,
        chat_repository=chat_repository,
    )

    send_user_message_use_case = providers.Factory(
        SendUserMessageUseCase,
        chat_repository=chat_repository,
        llm_queue_service=llm_queue_service,
    )
