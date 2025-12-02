# agents/doctor_assistant_agent.py
import requests
import json
from context_filter import is_medical_context, filter_response, create_medical_prompt, REJECTION_MESSAGE

class DoctorAssistantAgent:
    def __init__(self, message_bus=None):
        self.agent_id = "doctor_assistant"
        self.bus = message_bus
        
        if self.bus:
            self.bus.register(self.agent_id, self)

    def handle_message(self, message):
        if message.msg_type == "analyze_vitals":
            vitals = message.content
            return self.analyze_vitals(vitals)
        
        return {"error": "Unknown message type"}

    def analyze_vitals(self, vitals: dict):
        """Provide AI-powered medical analysis using Ollama"""
        
        heart_rate = vitals.get("heart_rate", 0)
        bp = vitals.get("bp", 0)
        spo2 = vitals.get("spo2", 0)
        glucose = vitals.get("glucose", 0)
        
        # Create medical-focused prompt
        context = f"Heart Rate: {heart_rate} bpm, BP: {bp} mmHg, SpO2: {spo2}%, Glucose: {glucose} mg/dL"
        prompt = create_medical_prompt(
            f"Analyze these vital signs: {context}",
            context
        )
        
        # Original prompt for structured output
        prompt = f"""You are MediBot AI, a specialized medical assistant. ONLY respond to medical and health questions.

Analyze these vital signs and provide a structured medical assessment:

Vital Signs:
- Heart Rate: {heart_rate} bpm
- Blood Pressure: {bp} mmHg (systolic)
- SpO2: {spo2}%
- Glucose: {glucose} mg/dL

Provide analysis in this exact JSON format:
{{
  "overall_status": "stable/concerning/critical",
  "risk_level": "low/medium/high",
  "medical_notes": ["list of clinical observations"],
  "recommendations": ["list of medical recommendations"],
  "follow_up": ["list of follow-up actions"]
}}

Be concise and medically accurate. Focus on actionable insights."""
        
        try:
            # Call Ollama API
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                ollama_response = response.json()
                ai_analysis = json.loads(ollama_response["response"])
                print(f"Ollama analysis: {ai_analysis}")
                return ai_analysis
            else:
                print(f"Ollama API error: {response.status_code}")
                return self._fallback_analysis(vitals)
                
        except Exception as e:
            print(f"Ollama connection failed: {e}")
            return self._fallback_analysis(vitals)
    
    def _fallback_analysis(self, vitals):
        """Fallback analysis if Ollama is unavailable"""
        heart_rate = vitals.get("heart_rate", 0)
        bp = vitals.get("bp", 0)
        spo2 = vitals.get("spo2", 0)
        glucose = vitals.get("glucose", 0)
        
        analysis = {
            "overall_status": "stable",
            "risk_level": "low",
            "medical_notes": [],
            "recommendations": [],
            "follow_up": ["Continue monitoring"]
        }
        
        # Basic rule-based analysis
        if heart_rate > 100 or bp > 140 or spo2 < 95 or glucose < 70:
            analysis["risk_level"] = "high"
            analysis["overall_status"] = "concerning"
            analysis["medical_notes"].append("Abnormal vital signs detected")
            analysis["recommendations"].append("Immediate medical attention required")
        elif heart_rate < 60 or bp < 90 or spo2 < 97 or glucose > 140:
            analysis["risk_level"] = "medium"
            analysis["medical_notes"].append("Some vitals outside normal range")
            analysis["recommendations"].append("Monitor closely")
        else:
            analysis["medical_notes"].append("All vitals within acceptable range")
            analysis["recommendations"].append("Continue standard care")
        
        return analysis