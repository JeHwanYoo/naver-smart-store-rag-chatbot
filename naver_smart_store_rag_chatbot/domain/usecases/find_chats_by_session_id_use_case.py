class FindChatsBySessionIdUseCase:
    def __init__(self, chat_repository):
        self.chat_repository = chat_repository
