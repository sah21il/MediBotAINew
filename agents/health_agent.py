import json
from models.health_chart_memory import HealthChartMemory
from ollama import chat

class HealthAgent:
    def __init__(self):
        with open("data/medical_chart_knowledge.txt", "r") as f:
            chart_text = f.read()
        self.chart_memory = HealthChartMemory(chart_text)

    def analyze_vitals(self, vitals: dict):
        """
        vitals = {
            "resp_rate": 28,
            "spo2": 90,
            "bp_sys": 180,
            "pulse": 130,
            "temp": 38.5,
            "consciousness": "Voice"
        }
        """
        # 1️⃣ Recall relevant rules from the medical chart
        context_rules = []
        for k in vitals.keys():
            context_rules += self.chart_memory.recall(f"{k} abnormal thresholds")

        # 2️⃣ Prepare reasoning prompt for LLM
        prompt = f"""
You are a medical assistant. Using these clinical guidelines:
{json.dumps(context_rules, indent=2)}

Given these vitals: {json.dumps(vitals)}

Decide what clinical action should be taken:
- MER Call
- MDT Review
- RN Review
- Normal Observation
Also, explain why briefly.
"""

        # 3️⃣ Query the local Ollama model (e.g., llama3, mistral, or your local model)
        response = chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        decision = response["message"]["content"]
        return decision
