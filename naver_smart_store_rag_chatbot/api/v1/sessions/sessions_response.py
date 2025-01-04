from dataclasses import dataclass
from typing import Dict


@dataclass
class SessionResponse:
    session_id: str
    first_message: str

    @staticmethod
    def from_dict(data: Dict) -> 'SessionResponse':
        return SessionResponse(
            **data,
        )
