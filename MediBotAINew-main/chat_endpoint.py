"""
Chat endpoint with medical context filtering and knowledge base
"""
import requests
from context_filter import is_medical_context, REJECTION_MESSAGE, create_medical_prompt
from medical_knowledge import get_vital_assessment, get_condition_info, get_medication_info, MEDICAL_KNOWLEDGE

def handle_chat(query: str) -> str:
    """Handle chat with medical knowledge base"""
    
    if not is_medical_context(query):
        return REJECTION_MESSAGE
    
    query_lower = query.lower()
    
    # Check for condition queries
    for condition in ["hypertension", "diabetes", "hypoxemia"]:
        if condition in query_lower:
            info = get_condition_info(condition)
            if info:
                return f"""**{condition.upper()}**

**Definition:** {info['definition']}

**Symptoms:** {info['symptoms']}

**Treatment:** {info['treatment']}

**Monitoring:** {info['monitoring']}

Consult your healthcare provider for personalized medical advice."""
    
    # Check for medication queries
    for med in ["metformin", "lisinopril", "amlodipine"]:
        if med in query_lower:
            info = get_medication_info(med)
            if info:
                return f"""**{med.upper()}**

**Class:** {info['class']}
**Indication:** {info['indication']}
**Typical Dosage:** {info['dosage']}
**Common Side Effects:** {info['side_effects']}
**Monitoring Required:** {info['monitoring']}

Always follow your doctor's prescription."""
    
    # Check for vital sign queries
    if "blood pressure" in query_lower or "bp" in query_lower:
        bp_info = MEDICAL_KNOWLEDGE["vital_signs"]["blood_pressure"]
        return f"""**BLOOD PRESSURE RANGES**

✅ **Normal:** {bp_info['normal']}
⚠️ **Elevated:** {bp_info['elevated']}
🟡 **Stage 1 Hypertension:** {bp_info['stage1_hypertension']}
🔴 **Stage 2 Hypertension:** {bp_info['stage2_hypertension']}
⬇️ **Hypotension:** {bp_info['hypotension']}
🚨 **Hypertensive Crisis:** {bp_info['crisis']}

Regular monitoring and lifestyle modifications are key."""
    
    if "heart rate" in query_lower or "pulse" in query_lower:
        hr_info = MEDICAL_KNOWLEDGE["vital_signs"]["heart_rate"]
        return f"""**HEART RATE RANGES**

✅ **Normal:** {hr_info['normal']}
⬇️ **Bradycardia:** {hr_info['low']}
⬆️ **Tachycardia:** {hr_info['high']}
🚨 **Critical Low:** {hr_info['critical_low']}
🚨 **Critical High:** {hr_info['critical_high']}

Consult a doctor if you experience persistent abnormal heart rates."""
    
    if "oxygen" in query_lower or "spo2" in query_lower:
        spo2_info = MEDICAL_KNOWLEDGE["vital_signs"]["spo2"]
        return f"""**OXYGEN SATURATION (SpO2) LEVELS**

✅ **Normal:** {spo2_info['normal']}
⚠️ **Mild Hypoxemia:** {spo2_info['mild_hypoxemia']}
🟡 **Moderate Hypoxemia:** {spo2_info['moderate_hypoxemia']}
🚨 **Severe Hypoxemia:** {spo2_info['severe_hypoxemia']}

Seek immediate medical attention if SpO2 drops below 90%."""
    
    if "glucose" in query_lower or "sugar" in query_lower:
        glucose_info = MEDICAL_KNOWLEDGE["vital_signs"]["glucose"]
        return f"""**BLOOD GLUCOSE LEVELS**

✅ **Normal Fasting:** {glucose_info['normal_fasting']}
⚠️ **Prediabetes:** {glucose_info['prediabetes']}
🔴 **Diabetes:** {glucose_info['diabetes']}
⬇️ **Hypoglycemia:** {glucose_info['hypoglycemia']}
🚨 **Severe Hypoglycemia:** {glucose_info['severe_hypoglycemia']}
⬆️ **Hyperglycemia:** {glucose_info['hyperglycemia']}

Regular monitoring and proper medication adherence are essential."""
    
    # Fallback to AI with enhanced medical context
    prompt = f"""You are MediBot AI, a medical assistant with comprehensive clinical knowledge.

Provide specific, evidence-based medical information. Include:
- Exact normal ranges for vital signs
- Specific medication names and dosages
- Clear clinical recommendations
- When to seek emergency care

User Question: {query}

Provide a detailed, clinically accurate response:"""
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "I can help with medical questions. Please ask about vital signs, symptoms, medications, or MediBot features."
            
    except Exception as e:
        return "I can help with medical questions. Please ask about vital signs, symptoms, medications, or MediBot features."
