# agents/health_agent.py

class HealthAgent:
    def __init__(self, message_bus=None):
        self.agent_id = "health_agent"
        self.bus = message_bus

        if self.bus:
            self.bus.register(self.agent_id, self)

    # -------------------------
    # Handle Messages
    # -------------------------
    def handle_message(self, message):
        if message.msg_type == "vitals_update":
            vitals = message.content
            print("[HealthAgent] Received vitals:", vitals)

            result = self.analyze_vitals(vitals)
            print("[HealthAgent] Analysis:", result)

            return result

        return {"error": "Unknown message type"}

    # -------------------------
    # Your ORIGINAL function
    # -------------------------
    def analyze_vitals(self, vitals: dict):

        resp = vitals["resp_rate"]
        spo2 = vitals["spo2"]
        bp = vitals["bp_sys"]
        pulse = vitals["pulse"]
        temp = vitals["temp"]
        consciousness = vitals["consciousness"]

        alerts = []

        if resp > 25:
            alerts.append("High respiration rate (tachypnea)")
        if spo2 < 92:
            alerts.append("Low oxygen saturation – possible hypoxia")
        if bp > 160:
            alerts.append("High blood pressure – hypertension risk")
        if pulse > 120:
            alerts.append("High pulse rate – tachycardia")
        if temp > 37.5:
            alerts.append("Fever detected")
        if consciousness.lower() != "alert":
            alerts.append("Altered consciousness level")

        if not alerts:
            return {"status": "normal", "warnings": []}

        return {
            "status": "critical",
            "warnings": alerts
        }
