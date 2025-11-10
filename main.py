from agents.health_agent import HealthAgent

agent = HealthAgent()

vitals = {
    "resp_rate": 28,
    "spo2": 90,
    "bp_sys": 180,
    "pulse": 130,
    "temp": 38.5,
    "consciousness": "Voice"
}

decision = agent.analyze_vitals(vitals)
print(decision)
