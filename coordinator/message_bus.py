from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Message:
    message_id: str
    sender_id: str
    receiver_id: str
    content: dict
    timestamp: datetime

    @classmethod
    def create(cls, sender_id, receiver_id, content):
        return cls(
            message_id=str(uuid.uuid4()),
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            timestamp=datetime.now()
        )
