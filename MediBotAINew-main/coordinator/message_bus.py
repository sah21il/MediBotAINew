# coordinator/message_bus.py

from coordinator.message import Message

class MessageBus:
    def __init__(self):
        self.agents = {}

    def register(self, agent_id, agent_instance):
        self.agents[agent_id] = agent_instance

    def send_and_wait(self, message: Message) -> Message:
        """Direct synchronous call to receiver agent."""
        receiver = self.agents.get(message.receiver)
        if not receiver:
            raise ValueError(f"Receiver agent not found: {message.receiver}")

        return receiver.handle_message(message)
