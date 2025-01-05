from dataclasses import dataclass
from typing import Dict


@dataclass
class ChatResponse:
    session_id: str
    user_message: str
    system_message: str

    @staticmethod
    def from_dict(data: Dict) -> 'ChatResponse':
        return ChatResponse(
            **data,
        )
