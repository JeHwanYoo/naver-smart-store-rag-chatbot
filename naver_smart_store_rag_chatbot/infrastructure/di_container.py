from dependency_injector import containers, providers

from naver_smart_store_rag_chatbot.domain.interfaces.repositories.chat_repository import ChatRepository
from naver_smart_store_rag_chatbot.domain.interfaces.repositories.chat_session_repository import ChatSessionRepository
from naver_smart_store_rag_chatbot.domain.usecases.find_all_chat_sessions_use_case import FindAllChatSessionsUseCase
from naver_smart_store_rag_chatbot.domain.usecases.find_chats_by_session_id_use_case import FindChatsBySessionIdUseCase


class Container(containers.DeclarativeContainer):
    chat_session_repository = providers.Dependency(instance_of=ChatSessionRepository)
    chat_repository = providers.Dependency(instance_of=ChatRepository)

    find_all_chat_sessions_use_case = providers.Factory(
        FindAllChatSessionsUseCase,
        chat_session_repository=chat_session_repository,
    )

    find_chats_by_session_id_use_case = providers.Factory(
        FindChatsBySessionIdUseCase,
        chat_repository=chat_repository,
    )
