from dataclasses import dataclass


@dataclass
class ChatSession:
    session_id: str
    first_message: str
