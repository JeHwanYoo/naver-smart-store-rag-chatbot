from dataclasses import dataclass


@dataclass
class SessionResponse:
    session_id: str
    first_message: str
