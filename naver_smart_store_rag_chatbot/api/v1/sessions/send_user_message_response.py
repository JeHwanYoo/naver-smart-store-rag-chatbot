from dataclasses import dataclass


@dataclass
class SendUserMessageResponse:
    session_id: str
    streaming_id: str
