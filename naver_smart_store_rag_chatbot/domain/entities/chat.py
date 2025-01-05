from dataclasses import dataclass


@dataclass
class Chat:
    session_id: str
    user_message: str
    system_message: str
