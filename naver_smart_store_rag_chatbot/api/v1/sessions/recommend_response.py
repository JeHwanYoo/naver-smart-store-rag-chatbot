from dataclasses import dataclass
from typing import List


@dataclass
class RecommendsResponse:
    session_id: str
    chatbot_recommends: List[str]
