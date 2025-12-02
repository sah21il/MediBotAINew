from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import random
import time
import math
# from gemini_client import get_gemini_response, get_medical_analysis

from agents.health_agent import HealthAgent
from agents.ingest_agent import IngestAgent
from agents.doctor_assistant_agent import DoctorAssistantAgent
from coordinator.message_bus import MessageBus
from coordinator.message import Message
from reports_agent import setup_reports_agent
from reminders_agent import setup_reminders_agent
from chat_endpoint import handle_chat
from medical_records_system import setup_medical_records_system

# Initialize FastAPI
app = FastAPI(title="MediBot AI Backend")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize agents
message_bus = MessageBus()
health_agent = HealthAgent(message_bus)
ingest_agent = IngestAgent("ingest_agent", {})
doctor_assistant = DoctorAssistantAgent(message_bus)

message_bus.register("health_agent", health_agent)
message_bus.register("ingest_agent", ingest_agent)
message_bus.register("doctor_assistant", doctor_assistant)

# Setup Reports Agent
setup_reports_agent(app)

# Setup Reminders Agent
setup_reminders_agent(app)

# Setup Medical Records System
setup_medical_records_system(app)

# ---------------------------
# Pydantic Models for API
# ---------------------------
class VitalsInput(BaseModel):
    resp_rate: float
    spo2: float
    bp_sys: float
    pulse: float
    temp: float
    consciousness: str

# ---------------------------
# API ROUTES
# ---------------------------

@app.get("/")
def home():
    return {"message": "MediBot Backend Running"}

@app.post("/api/health/analyze")
def analyze_vitals(vitals: VitalsInput):
    """
    FRONTEND calls this endpoint
    → agent.analyze_vitals()
    → returns recommendations
    """
    vitals_dict = vitals.dict()
    result = health_agent.analyze_vitals(vitals_dict)
    
    # Convert to frontend format and store
    frontend_vitals = {
        "heart_rate": vitals_dict["pulse"],
        "bp": vitals_dict["bp_sys"], 
        "spo2": vitals_dict["spo2"],
        "glucose": 100  # Default value since not provided
    }
    ingest_agent.latest = frontend_vitals
    print(f"Stored vitals: {frontend_vitals}")  # Debug log
    
    return {"analysis": result}

@app.post("/ingest")
def ingest_data(data: dict):
    """
    General ingestion agent
    """
    result = ingest_agent.ingest(data)
    return {"status": "success", "processed": result}

@app.get("/ingest/latest")
def latest_data():
    try:
        # Fetch from real mock APIs for base values
        user_response = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=1)
        
        if user_response.status_code == 200:
            user_data = user_response.json()
            base_seed = len(user_data.get('name', ''))
        else:
            base_seed = 10
            
    except Exception as e:
        print(f"API fetch failed: {e}")
        base_seed = 10
    
    # Create realistic variations using time-based sine waves + API seed
    current_time = time.time()
    
    # Occasionally generate critical values for alarm testing
    critical_chance = random.random()
    
    if critical_chance < 0.1:  # 10% chance of critical values
        vitals = {
            "heart_rate": random.choice([40, 140]),  # Critical values
            "bp": random.choice([60, 200]),
            "spo2": random.choice([80, 100]),
            "glucose": random.choice([40, 300])
        }
    else:
        # Normal realistic medical values
        vitals = {
            "heart_rate": max(50, min(120, round(75 + 
                               10 * math.sin(current_time / 30) + 
                               random.uniform(-8, 8), 1))),  # 50-120 bpm
            
            "bp": max(80, min(180, round(120 + 
                       15 * math.sin(current_time / 45) + 
                       random.uniform(-12, 12), 1))),  # 80-180 mmHg
            
            "spo2": max(88, min(100, round(97 + 
                         2 * math.sin(current_time / 60) + 
                         random.uniform(-3, 2), 1))),  # 88-100%
            
            "glucose": max(60, min(200, round(100 + 
                            20 * math.sin(current_time / 90) + 
                            random.uniform(-15, 25), 1)))  # 60-200 mg/dL
        }
    
    print(f"Generated vitals with deviations: {vitals}")
    return {"latest": vitals}

@app.post("/api/doctor-assistant/analyze")
def analyze_vitals_assistant(request: dict):
    """
    Doctor Assistant analysis endpoint
    """
    vitals = request.get("vitals", {})
    analysis = doctor_assistant.analyze_vitals(vitals)
    return {"analysis": analysis}

@app.post("/api/doctor-assistant/chat")
def chat_with_assistant(request: dict):
    """
    Chat endpoint with medical context filtering
    """
    query = request.get("message", "")
    response = handle_chat(query)
    return {"response": response}


