from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import random
import time
import math

from agents.health_agent import HealthAgent
from agents.ingest_agent import IngestAgent
from agents.doctor_assistant_agent import DoctorAssistantAgent
from coordinator.message_bus import MessageBus
from coordinator.message import Message

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
        user_response = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=3)
        
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
    
    # Create values that will show deviations (some normal, some abnormal)
    vitals = {
        "heart_rate": round(75 + base_seed % 30 + 
                           15 * math.sin(current_time / 30) + 
                           random.uniform(-5, 5), 1),  # Can go 50-120
        
        "bp": round(120 + base_seed % 40 + 
                   25 * math.sin(current_time / 45) + 
                   random.uniform(-10, 10), 1),  # Can go 85-185
        
        "spo2": round(96 + base_seed % 6 + 
                     3 * math.sin(current_time / 60) + 
                     random.uniform(-2, 2), 1),  # Can go 91-105
        
        "glucose": round(100 + base_seed % 50 + 
                        30 * math.sin(current_time / 120) + 
                        random.uniform(-15, 15), 1)  # Can go 55-195
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


