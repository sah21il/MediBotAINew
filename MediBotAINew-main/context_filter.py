"""
Context Filter - Restricts AI responses to medical and project-related queries only
"""

ALLOWED_TOPICS = [
    "medical", "health", "vital signs", "heart rate", "blood pressure", "spo2", "oxygen",
    "glucose", "diabetes", "hypertension", "medication", "symptoms", "diagnosis", "treatment",
    "patient", "doctor", "hospital", "clinic", "emergency", "disease", "illness", "pain",
    "fever", "temperature", "pulse", "breathing", "respiratory", "cardiac", "prescription",
    "reminder", "appointment", "checkup", "monitoring", "report", "test results", "lab",
    "medibot", "dashboard", "agent", "alarm", "notification", "vitals"
]

REJECTION_MESSAGE = """I am MediBot AI, a specialized medical assistant. I can only help with:

🏥 Medical & Health Questions
- Vital signs analysis (heart rate, BP, SpO2, glucose)
- Symptoms and health concerns
- Medication reminders and management
- Medical reports and test results

📊 MediBot Features
- Health monitoring and alarms
- Smart reminders system
- Doctor assistant chat
- Report analysis

Please ask me questions related to healthcare or MediBot features."""

def is_medical_context(query: str) -> bool:
    """Check if query is related to medical/health topics"""
    query_lower = query.lower()
    
    # Check for allowed medical keywords
    for topic in ALLOWED_TOPICS:
        if topic in query_lower:
            return True
    
    # Reject common non-medical queries
    non_medical = ["weather", "sports", "politics", "entertainment", "movie", "game", 
                   "recipe", "cooking", "travel", "joke", "story", "news"]
    
    for topic in non_medical:
        if topic in query_lower:
            return False
    
    # If unclear, allow (to avoid false rejections)
    return True

def filter_response(query: str, response: str) -> str:
    """Filter AI response based on query context"""
    if not is_medical_context(query):
        return REJECTION_MESSAGE
    
    return response

def create_medical_prompt(user_query: str, context: str = "") -> str:
    """Create a medical-focused prompt with context restrictions"""
    
    system_context = """You are MediBot AI, a specialized medical assistant for the MediBot Health Monitoring System.

YOUR ROLE:
- Analyze vital signs (heart rate, blood pressure, SpO2, glucose, temperature)
- Provide medical recommendations and health advice
- Help with medication reminders and health monitoring
- Answer questions about MediBot features and functionality

STRICT RULES:
- ONLY answer medical, health, or MediBot-related questions
- If asked about non-medical topics (weather, sports, politics, entertainment, etc.), respond: "I can only assist with medical and health-related questions."
- Always prioritize patient safety and recommend professional medical consultation when needed
- Provide evidence-based medical information
- Be concise and actionable

CONTEXT: {context}

USER QUERY: {query}

Provide a helpful, medically-focused response:"""
    
    return system_context.format(context=context, query=user_query)
