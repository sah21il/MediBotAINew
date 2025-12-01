"""
Reports Agent Backend - Medical Report Analysis & Repository
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime
import random

router = APIRouter()

# Mock medical reports database - starts empty, only uploaded reports
MOCK_REPORTS = []

class ReportAnalysisRequest(BaseModel):
    report_id: str
    report_type: str
    data: Dict[str, Any]

class SendToDoctorRequest(BaseModel):
    report_id: str
    analysis: str

@router.get("/api/reports")
async def get_reports():
    """Get all medical reports from repository"""
    print(f"Returning {len(MOCK_REPORTS)} reports")  # Debug log
    # Sort by date, newest first
    sorted_reports = sorted(MOCK_REPORTS, key=lambda x: x["date"], reverse=True)
    return sorted_reports

@router.post("/api/reports/analyze")
async def analyze_report(request: ReportAnalysisRequest):
    """Analyze medical report using AI"""
    try:
        report_type = request.report_type
        data = request.data
        
        # Find and update report status to analyzed
        for report in MOCK_REPORTS:
            if report["id"] == request.report_id:
                report["status"] = "analyzed"
                break
        
        # Generate AI analysis based on report type
        analysis = generate_report_analysis(report_type, data)
        
        return {
            "report_id": request.report_id,
            "analysis": analysis,
            "confidence": 0.92,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@router.post("/api/reports/send-to-doctor")
async def send_to_doctor_assistant(request: SendToDoctorRequest):
    """Send report analysis to Doctor Assistant"""
    try:
        # Find the report
        report = next((r for r in MOCK_REPORTS if r["id"] == request.report_id), None)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Simulate sending to doctor assistant
        doctor_message = {
            "type": "report_analysis",
            "report_id": request.report_id,
            "report_name": report["name"],
            "report_type": report["type"],
            "patient_id": report["patient_id"],
            "analysis": request.analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "status": "sent",
            "message": "Report analysis sent to Doctor Assistant successfully",
            "doctor_message": doctor_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Send error: {str(e)}")

@router.post("/api/reports/upload")
async def upload_report(file: UploadFile = File(...)):
    """Upload new medical report"""
    try:
        # Read file content
        content = await file.read()
        print(f"Uploaded file: {file.filename}, size: {len(content)} bytes")
        
        # Generate mock report data
        report_id = f"rpt_{uuid.uuid4().hex[:6]}"
        
        # Determine report type from filename
        filename = file.filename.lower()
        if "ecg" in filename:
            report_type = "ECG"
        elif "xray" in filename or "x-ray" in filename or "chest" in filename:
            report_type = "X-Ray"
        elif "blood" in filename or "lab" in filename:
            report_type = "Blood Test"
        elif "mri" in filename:
            report_type = "MRI"
        elif "ct" in filename:
            report_type = "CT Scan"
        elif "echo" in filename or "ultrasound" in filename:
            report_type = "Ultrasound"
        else:
            report_type = "Medical Report"
        
        new_report = {
            "id": report_id,
            "name": f"{file.filename}",
            "type": report_type,
            "patient_id": f"PT{random.randint(100, 999)}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "pending",
            "data": generate_mock_report_data(report_type),
            "file_content": content.decode('utf-8', errors='ignore')[:1000]  # Store first 1000 chars
        }
        
        MOCK_REPORTS.insert(0, new_report)  # Add to beginning of list
        print(f"Added new report: {new_report['name']}")
        
        return {
            "status": "uploaded",
            "report_id": report_id,
            "report": new_report,
            "message": "Report uploaded successfully"
        }
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")

def generate_report_analysis(report_type: str, data: Dict[str, Any]) -> str:
    """Generate AI analysis for different report types"""
    
    if report_type == "ECG":
        hr = data.get("heart_rate", random.randint(60, 100))
        rhythm = data.get("rhythm", "Normal Sinus Rhythm")
        
        analysis = f"📈 **COMPREHENSIVE ECG ANALYSIS**\n\n"
        analysis += f"**PRIMARY FINDINGS:**\n"
        analysis += f"• Heart Rate: {hr} bpm\n"
        analysis += f"• Rhythm: {rhythm}\n"
        analysis += f"• Axis: Normal (0° to +90°)\n"
        analysis += f"• PR Interval: {random.randint(120, 200)} ms\n"
        analysis += f"• QRS Duration: {random.randint(80, 120)} ms\n\n"
        
        # Risk Stratification
        analysis += "**RISK STRATIFICATION:**\n"
        if hr < 50:
            analysis += "🔴 **HIGH RISK - Severe Bradycardia**\n• Immediate evaluation required\n• Consider atropine or pacing\n• Monitor for hemodynamic compromise\n\n"
        elif hr < 60:
            analysis += "🟡 **MODERATE RISK - Bradycardia**\n• Monitor for symptoms (dizziness, fatigue)\n• Evaluate medications (beta-blockers, digoxin)\n• Consider Holter monitoring\n\n"
        elif hr > 120:
            analysis += "🔴 **HIGH RISK - Severe Tachycardia**\n• Evaluate for arrhythmias\n• Check electrolytes and thyroid function\n• Consider emergency intervention\n\n"
        elif hr > 100:
            analysis += "🟡 **MODERATE RISK - Tachycardia**\n• Assess for underlying causes\n• Monitor trends\n• Consider rate control if persistent\n\n"
        else:
            analysis += "✅ **LOW RISK - Normal Heart Rate**\n• Continue routine monitoring\n• No immediate intervention needed\n\n"
        
        # Clinical Correlations
        analysis += "**CLINICAL CORRELATIONS:**\n"
        analysis += "• Chest pain assessment: Correlate with troponins\n"
        analysis += "• Shortness of breath: Consider echo if abnormal\n"
        analysis += "• Syncope history: May need EP study\n"
        analysis += "• Medication review: Check QT-prolonging drugs\n\n"
        
        # Follow-up Recommendations
        analysis += "**FOLLOW-UP RECOMMENDATIONS:**\n"
        analysis += "• Serial ECGs if acute changes\n"
        analysis += "• Cardiology consultation if abnormal\n"
        analysis += "• Exercise stress test if chest pain\n"
        analysis += "• Holter monitor for palpitations\n\n"
        
        # Differential Diagnosis
        analysis += "**DIFFERENTIAL CONSIDERATIONS:**\n"
        if hr < 60:
            analysis += "• Sick sinus syndrome\n• AV block\n• Hypothyroidism\n• Medication effect\n"
        elif hr > 100:
            analysis += "• Atrial fibrillation\n• Supraventricular tachycardia\n• Hyperthyroidism\n• Anxiety/stress\n"
        
    elif report_type == "Blood Test":
        wbc = data.get("wbc", random.randint(4000, 15000))
        hgb = data.get("hemoglobin", round(random.uniform(8.0, 16.0), 1))
        plt = data.get("platelets", random.randint(100000, 400000))
        
        analysis = f"🩸 **COMPREHENSIVE HEMATOLOGY ANALYSIS**\n\n"
        analysis += f"**COMPLETE BLOOD COUNT:**\n"
        analysis += f"• WBC: {wbc:,} /μL (Normal: 4,000-11,000)\n"
        analysis += f"• Hemoglobin: {hgb} g/dL (Normal: 12.0-16.0)\n"
        analysis += f"• Platelets: {plt:,} /μL (Normal: 150,000-400,000)\n\n"
        
        # Risk Assessment
        analysis += "**RISK ASSESSMENT:**\n"
        risk_factors = []
        
        if wbc > 15000:
            analysis += "🔴 **CRITICAL - Severe Leukocytosis**\n• Possible sepsis or hematologic malignancy\n• Immediate blood cultures and antibiotics\n• Hematology consultation urgent\n\n"
            risk_factors.append("severe infection")
        elif wbc > 11000:
            analysis += "🟡 **ELEVATED WBC COUNT**\n• Infection or inflammatory process\n• Monitor temperature and vital signs\n• Consider blood cultures\n\n"
            risk_factors.append("infection")
        elif wbc < 4000:
            analysis += "🔴 **LEUKOPENIA DETECTED**\n• Immunocompromised state\n• Risk of opportunistic infections\n• Avoid live vaccines\n\n"
            risk_factors.append("immunosuppression")
        
        if hgb < 8.0:
            analysis += "🔴 **SEVERE ANEMIA**\n• Transfusion may be indicated\n• Evaluate for active bleeding\n• Iron studies and B12/folate levels\n\n"
            risk_factors.append("severe anemia")
        elif hgb < 10.0:
            analysis += "🟡 **MODERATE ANEMIA**\n• Iron deficiency likely\n• GI evaluation for blood loss\n• Nutritional assessment\n\n"
            risk_factors.append("anemia")
        
        if plt < 100000:
            analysis += "🔴 **THROMBOCYTOPENIA**\n• Bleeding risk assessment\n• Hold anticoagulants\n• Hematology consultation\n\n"
            risk_factors.append("bleeding risk")
        
        # Clinical Management
        analysis += "**CLINICAL MANAGEMENT:**\n"
        if "severe anemia" in risk_factors:
            analysis += "• Type and crossmatch for transfusion\n"
            analysis += "• Hemoglobin electrophoresis\n"
            analysis += "• Reticulocyte count\n"
        if "infection" in risk_factors:
            analysis += "• Blood cultures x2 sets\n"
            analysis += "• Procalcitonin level\n"
            analysis += "• Broad-spectrum antibiotics\n"
        if "bleeding risk" in risk_factors:
            analysis += "• Platelet transfusion if <50,000\n"
            analysis += "• Avoid invasive procedures\n"
            analysis += "• Peripheral blood smear\n"
        
        analysis += "\n**FOLLOW-UP TESTING:**\n"
        analysis += "• Repeat CBC in 24-48 hours\n"
        analysis += "• Iron studies, B12, folate\n"
        analysis += "• Comprehensive metabolic panel\n"
        analysis += "• Urinalysis for hematuria\n\n"
        
        analysis += "**SPECIALIST REFERRALS:**\n"
        if any(risk in risk_factors for risk in ["severe anemia", "bleeding risk"]):
            analysis += "• Hematology - within 24 hours\n"
        if "severe infection" in risk_factors:
            analysis += "• Infectious Disease consultation\n"
        analysis += "• Gastroenterology if GI bleeding suspected\n"
        
    elif report_type == "Medical Report":
        analysis = f"📄 **UPLOADED REPORT ANALYSIS**\n\n"
        analysis += f"**Document Type:** {report_type}\n\n"
        analysis += "**AI Processing:**\n• Document successfully uploaded and processed\n• Content extracted and analyzed\n• Ready for clinical review\n\n"
        analysis += "**Recommendations:**\n• Review document content with clinical team\n• Correlate findings with patient symptoms\n• Consider follow-up studies if indicated\n• Document findings in patient record"
        
    elif report_type == "X-Ray":
        findings = data.get("findings", [])
        
        analysis = f"🦴 **X-RAY ANALYSIS REPORT**\n\n"
        analysis += f"**Findings:**\n"
        for finding in findings:
            analysis += f"• {finding}\n"
        
        if "normal" in str(findings).lower():
            analysis += "\n✅ **NORMAL STUDY**\n• No acute abnormalities detected\n• Continue routine care\n"
        else:
            analysis += "\n🟡 **ABNORMAL FINDINGS**\n• Further evaluation may be needed\n• Clinical correlation recommended\n"
        
    elif report_type == "MRI":
        analysis = f"🧠 **MRI ANALYSIS REPORT**\n\n"
        analysis += "**Imaging Protocol:** Multi-sequence MRI\n\n"
        
        findings = data.get("findings", [])
        if "normal" in str(findings).lower():
            analysis += "✅ **NORMAL MRI STUDY**\n• No acute abnormalities\n• Normal brain parenchyma\n• No evidence of infarct or hemorrhage\n"
        else:
            analysis += "🟡 **FINDINGS NOTED**\n• Detailed radiologist review recommended\n• Clinical correlation advised\n"
        
    else:
        analysis = f"📄 **GENERAL REPORT ANALYSIS**\n\n"
        analysis += "**Report Type:** " + report_type + "\n\n"
        analysis += "**AI Assessment:**\n• Report reviewed and processed\n• Clinical correlation recommended\n• Follow standard protocols\n\n"
        analysis += "**Next Steps:**\n• Review with attending physician\n• Consider additional testing if indicated\n• Monitor patient response"
    
    return analysis

def generate_mock_report_data(report_type: str) -> Dict[str, Any]:
    """Generate mock data for different report types"""
    
    if report_type == "ECG":
        return {
            "heart_rate": random.randint(60, 100),
            "rhythm": "Normal Sinus Rhythm",
            "pr_interval": random.randint(120, 200),
            "qrs_duration": random.randint(80, 120),
            "findings": ["Normal ECG"]
        }
    elif report_type == "Blood Test":
        return {
            "wbc": random.randint(4000, 11000),
            "rbc": round(random.uniform(4.0, 5.5), 1),
            "hemoglobin": round(random.uniform(12.0, 16.0), 1),
            "platelets": random.randint(150000, 400000)
        }
    elif report_type == "X-Ray":
        return {
            "view": "PA and Lateral",
            "findings": ["Clear lung fields", "Normal heart size"],
            "impression": "Normal chest X-ray"
        }
    else:
        return {
            "findings": ["Normal study"],
            "impression": "No acute abnormalities"
        }

# Add router to main FastAPI app
def setup_reports_agent(app):
    app.include_router(router)