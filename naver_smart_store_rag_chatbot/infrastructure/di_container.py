from dependency_injector import containers, providers

from naver_smart_store_rag_chatbot.domain.interfaces.chat_session_repository import ChatSessionRepository
from naver_smart_store_rag_chatbot.domain.usecases.find_all_chat_sessions_use_case import FindAllChatSessionsUseCase


class Container(containers.DeclarativeContainer):
    chat_session_repository = providers.Dependency(instance_of=ChatSessionRepository)

    find_all_chat_sessions_use_case = providers.Factory(
        FindAllChatSessionsUseCase,
        chat_session_repository=chat_session_repository,
    )
