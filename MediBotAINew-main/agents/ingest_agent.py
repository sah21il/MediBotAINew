import requests
from coordinator.message import Message

class IngestAgent:
    def __init__(self, agent_id, api_sources):
        self.agent_id = agent_id
        self.api_sources = api_sources
        self.latest = {}

    def poll_sources(self):
        """Fetch all external API vitals."""
        collected = {}
        for key, url in self.api_sources.items():
            try:
                r = requests.get(url, timeout=2)
                collected[key] = r.json().get("value", None)
            except:
                collected[key] = None

        self.latest = collected
        return collected

    def handle_message(self, message: Message):
        if message.msg_type == "get_latest":
            return self.latest
        
        return {"error": "Unknown message"}
