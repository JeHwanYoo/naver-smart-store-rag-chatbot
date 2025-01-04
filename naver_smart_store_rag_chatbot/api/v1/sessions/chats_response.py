from dataclasses import dataclass


@dataclass
class ChatResponse:
    session_id: str
    user_message: str
    system_message: str
