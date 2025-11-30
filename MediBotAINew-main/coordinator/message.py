# coordinator/message.py

from datetime import datetime
import uuid

class Message:
    def __init__(self, sender, receiver, msg_type, content, priority=1):
        self.message_id = str(uuid.uuid4())
        self.conversation_id = str(uuid.uuid4())
        self.sender = sender
        self.receiver = receiver
        self.msg_type = msg_type
        self.content = content
        self.priority = priority
        self.timestamp = datetime.utcnow()
        self.processed = False

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "msg_type": self.msg_type,
            "content": self.content,
            "priority": self.priority,
            "timestamp": self.timestamp.isoformat(),
        }
