"""
Enhanced Doctor Assistant API with Medical Knowledge Integration
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
import random
from medical_knowledge import get_medical_response, analyze_vitals_comprehensive, CLINICAL_SCENARIOS

router = APIRouter()

class VitalSigns(BaseModel):
    heart_rate: Optional[float] = None
    bp: Optional[float] = None
    spo2: Optional[float] = None
    glucose: Optional[float] = None
    temperature: Optional[float] = None
    resp_rate: Optional[float] = None

class ChatRequest(BaseModel):
    message: str
    vitals: Optional[Dict[str, Any]] = None
    context: Optional[str] = None

class AnalysisRequest(BaseModel):
    vitals: Dict[str, Any]
    symptoms: Optional[str] = None
    history: Optional[str] = None

@router.post("/api/doctor-assistant/chat")
async def enhanced_chat(request: ChatRequest):
    """Enhanced chat endpoint with medical knowledge"""
    try:
        # Get medical response using knowledge base
        response = get_medical_response(request.message, request.vitals)
        
        return {
            "response": response,
            "confidence": 0.95,
            "sources": ["Medical Knowledge Base", "Clinical Guidelines"],
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")

@router.post("/api/doctor-assistant/analyze")
async def enhanced_analysis(request: AnalysisRequest):
    """Enhanced vital signs analysis with clinical context"""
    try:
        vitals = request.vitals
        
        # Comprehensive analysis
        analysis_parts = []
        
        # Heart rate analysis
        hr = vitals.get('heart_rate', 0)
        if hr < 50:
            analysis_parts.append("🔴 CRITICAL: Severe bradycardia detected. Consider atropine or pacing.")
        elif hr < 60:
            analysis_parts.append("🟡 Bradycardia present. Monitor for symptoms of decreased cardiac output.")
        elif hr > 120:
            analysis_parts.append("🔴 Significant tachycardia. Evaluate for underlying causes (fever, dehydration, arrhythmia).")
        elif hr > 100:
            analysis_parts.append("🟡 Mild tachycardia. Consider causes: anxiety, pain, medications.")
        else:
            analysis_parts.append("✅ Heart rate within normal limits.")
        
        # Blood pressure analysis
        bp = vitals.get('bp', 0)
        if bp > 180:
            analysis_parts.append("🔴 HYPERTENSIVE CRISIS: Immediate intervention required. Consider IV antihypertensives.")
        elif bp > 140:
            analysis_parts.append("🟡 Stage 2 hypertension. Evaluate for target organ damage.")
        elif bp < 80:
            analysis_parts.append("🔴 Severe hypotension. Assess for shock, consider fluid resuscitation.")
        elif bp < 90:
            analysis_parts.append("🟡 Hypotension present. Monitor closely, evaluate causes.")
        else:
            analysis_parts.append("✅ Blood pressure within acceptable range.")
        
        # Oxygen saturation
        spo2 = vitals.get('spo2', 0)
        if spo2 < 85:
            analysis_parts.append("🔴 CRITICAL: Severe hypoxemia. Immediate oxygen therapy and respiratory support needed.")
        elif spo2 < 90:
            analysis_parts.append("🔴 Moderate hypoxemia. High-flow oxygen therapy indicated.")
        elif spo2 < 95:
            analysis_parts.append("🟡 Mild hypoxemia. Supplemental oxygen may be beneficial.")
        else:
            analysis_parts.append("✅ Oxygen saturation adequate.")
        
        # Glucose analysis
        glucose = vitals.get('glucose', 0)
        if glucose > 250:
            analysis_parts.append("🔴 Severe hyperglycemia. Check for DKA, consider insulin therapy.")
        elif glucose > 180:
            analysis_parts.append("🟡 Hyperglycemia present. Monitor for complications.")
        elif glucose < 60:
            analysis_parts.append("🔴 Hypoglycemia detected. Immediate glucose administration needed.")
        elif glucose < 70:
            analysis_parts.append("🟡 Mild hypoglycemia. Monitor closely, consider glucose supplementation.")
        else:
            analysis_parts.append("✅ Glucose levels within normal range.")
        
        # Risk stratification
        risk_factors = []
        if hr < 50 or hr > 120: risk_factors.append("cardiac")
        if bp > 180 or bp < 80: risk_factors.append("hemodynamic")
        if spo2 < 90: risk_factors.append("respiratory")
        if glucose < 60 or glucose > 250: risk_factors.append("metabolic")
        
        risk_level = "HIGH" if len(risk_factors) >= 2 else "MODERATE" if len(risk_factors) == 1 else "LOW"
        
        # Clinical recommendations
        recommendations = []
        if risk_level == "HIGH":
            recommendations.extend([
                "Continuous monitoring required",
                "Consider ICU consultation",
                "Frequent vital sign checks (q15min)",
                "Prepare for potential interventions"
            ])
        elif risk_level == "MODERATE":
            recommendations.extend([
                "Enhanced monitoring (q30min)",
                "Trending vital signs",
                "Consider additional diagnostics",
                "Notify physician of changes"
            ])
        else:
            recommendations.extend([
                "Continue routine monitoring",
                "Document trends",
                "Standard care protocols"
            ])
        
        analysis = "\\n".join(analysis_parts)
        
        return {
            "analysis": analysis,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "confidence": 0.92,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@router.get("/api/doctor-assistant/protocols/{protocol_name}")
async def get_clinical_protocol(protocol_name: str):
    """Get specific clinical protocols"""
    protocols = {
        "sepsis": {
            "name": "Sepsis Management Protocol",
            "steps": [
                "Recognize sepsis using qSOFA or SIRS criteria",
                "Obtain blood cultures before antibiotics",
                "Administer broad-spectrum antibiotics within 1 hour",
                "Fluid resuscitation: 30ml/kg crystalloid",
                "Monitor lactate levels",
                "Consider vasopressors if hypotensive after fluids"
            ],
            "timeframes": {
                "antibiotics": "1 hour",
                "cultures": "Before antibiotics",
                "fluids": "Within 3 hours"
            }
        },
        "stroke": {
            "name": "Acute Stroke Protocol",
            "steps": [
                "FAST assessment (Face, Arms, Speech, Time)",
                "Immediate CT head without contrast",
                "Check blood glucose",
                "Assess for tPA eligibility",
                "Blood pressure management",
                "Neurological monitoring"
            ],
            "timeframes": {
                "ct_scan": "Within 25 minutes",
                "tpa_decision": "Within 60 minutes",
                "door_to_needle": "Within 60 minutes"
            }
        },
        "cardiac_arrest": {
            "name": "Cardiac Arrest Protocol (ACLS)",
            "steps": [
                "Check responsiveness and pulse",
                "Begin high-quality CPR (30:2 ratio)",
                "Apply AED/defibrillator",
                "Establish advanced airway",
                "Administer epinephrine every 3-5 minutes",
                "Consider reversible causes (H's and T's)"
            ],
            "medications": {
                "epinephrine": "1mg IV/IO every 3-5 minutes",
                "amiodarone": "300mg IV for VF/VT",
                "atropine": "Removed from ACLS 2020"
            }
        }
    }
    
    if protocol_name.lower() not in protocols:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    return protocols[protocol_name.lower()]

@router.get("/api/doctor-assistant/drug-info/{drug_name}")
async def get_drug_information(drug_name: str):
    """Get medication information"""
    drugs = {
        "metoprolol": {
            "class": "Beta-blocker",
            "indications": ["Hypertension", "Angina", "Heart failure", "Post-MI"],
            "mechanism": "Selective beta-1 receptor antagonist",
            "dosing": {
                "hypertension": "25-100mg BID",
                "heart_failure": "12.5-200mg BID",
                "post_mi": "25-200mg BID"
            },
            "contraindications": ["Severe bradycardia", "Heart block", "Cardiogenic shock"],
            "side_effects": ["Bradycardia", "Fatigue", "Dizziness", "Depression"],
            "monitoring": ["Heart rate", "Blood pressure", "Signs of heart failure"]
        },
        "lisinopril": {
            "class": "ACE Inhibitor",
            "indications": ["Hypertension", "Heart failure", "Post-MI", "Diabetic nephropathy"],
            "mechanism": "Inhibits angiotensin-converting enzyme",
            "dosing": {
                "hypertension": "10-40mg daily",
                "heart_failure": "5-40mg daily",
                "post_mi": "5-10mg daily"
            },
            "contraindications": ["Pregnancy", "Angioedema history", "Bilateral renal artery stenosis"],
            "side_effects": ["Dry cough", "Hyperkalemia", "Angioedema", "Hypotension"],
            "monitoring": ["Kidney function", "Potassium", "Blood pressure"]
        }
    }
    
    drug_lower = drug_name.lower()
    if drug_lower not in drugs:
        return {
            "message": f"Detailed information for {drug_name} not available in current database.",
            "suggestion": "Please consult drug reference or pharmacist for complete information."
        }
    
    return drugs[drug_lower]

# Add router to main FastAPI app
def setup_enhanced_doctor_assistant(app):
    app.include_router(router)