from dataclasses import dataclass


@dataclass
class SessionsResponse:
    session_id: str
    first_message: str
