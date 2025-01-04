from dataclasses import dataclass


@dataclass
class SendUserMessageRequest:
    user_message: str
