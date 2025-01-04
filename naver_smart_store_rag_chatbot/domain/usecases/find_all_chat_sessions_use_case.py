class FindAllChatSessionsUseCase:
    def __init__(self, chat_session_repository):
        self.chat_session_repository = chat_session_repository
