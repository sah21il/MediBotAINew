"""
Centralized Medical Records System - Cloud-based report storage and retrieval
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import json
import os
import base64
from supabase_storage import get_supabase_storage

router = APIRouter()

# Supabase Cloud Storage
RECORDS_DATABASE = []

# Initialize Supabase
try:
    storage = get_supabase_storage()
    USE_CLOUD = True
except Exception as e:
    print(f"Supabase not configured, using local storage: {e}")
    USE_CLOUD = False
    CLOUD_STORAGE_PATH = "cloud_medical_records"
    os.makedirs(CLOUD_STORAGE_PATH, exist_ok=True)

class MedicalRecord(BaseModel):
    patient_id: str
    patient_name: str
    test_type: str
    lab_name: str
    test_date: str
    notes: Optional[str] = ""

class RecordResponse(BaseModel):
    record_id: str
    patient_id: str
    patient_name: str
    test_type: str
    lab_name: str
    test_date: str
    upload_date: str
    file_name: str
    file_size: int
    notes: str
    ai_summary: Optional[str] = ""

@router.post("/api/medical-records/upload")
async def upload_medical_record(
    file: UploadFile = File(...),
    patient_id: str = Form(""),
    patient_name: str = Form(""),
    test_type: str = Form(""),
    lab_name: str = Form(""),
    test_date: str = Form(""),
    notes: str = Form("")
):
    """Upload medical report to centralized cloud storage"""
    
    print(f"\n=== UPLOAD DEBUG ===")
    print(f"File: {file.filename}")
    print(f"Patient Name: '{patient_name}'")
    print(f"Patient ID: '{patient_id}'")
    print(f"Test Type: '{test_type}'")
    print(f"Lab Name: '{lab_name}'")
    print(f"Test Date: '{test_date}'")
    print(f"Notes: '{notes}'")
    print(f"===================\n")
    
    try:
        # Generate unique record ID
        record_id = f"MR_{uuid.uuid4().hex[:8].upper()}"
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Save to Supabase cloud storage
        file_path = f"{record_id}_{file.filename}"
        
        if USE_CLOUD:
            public_url = storage.upload_file(file_content, file_path)
        else:
            # Fallback to local storage
            local_path = os.path.join(CLOUD_STORAGE_PATH, file_path)
            with open(local_path, "wb") as f:
                f.write(file_content)
            public_url = f"local://{local_path}"
        
        # Create record metadata
        record = {
            "record_id": record_id,
            "patient_id": patient_id or f"PAT_{uuid.uuid4().hex[:6].upper()}",
            "patient_name": patient_name,
            "test_type": test_type,
            "lab_name": lab_name,
            "test_date": test_date,
            "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_name": file.filename,
            "file_path": file_path,
            "file_size": file_size,
            "notes": notes,
            "ai_summary": generate_ai_summary(test_type, file.filename),
            "cloud_url": public_url,
            "storage_type": "supabase" if USE_CLOUD else "local"
        }
        
        # Store in database
        RECORDS_DATABASE.append(record)
        
        return {
            "success": True,
            "message": "Medical record uploaded successfully",
            "record": record
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/api/medical-records/list")
async def list_medical_records(patient_id: Optional[str] = None):
    """List all medical records or filter by patient ID"""
    
    if patient_id:
        filtered_records = [r for r in RECORDS_DATABASE if r["patient_id"] == patient_id]
        return {
            "total": len(filtered_records),
            "records": filtered_records
        }
    
    return {
        "total": len(RECORDS_DATABASE),
        "records": RECORDS_DATABASE
    }

@router.get("/api/medical-records/{record_id}")
async def get_medical_record(record_id: str):
    """Get specific medical record details"""
    
    for record in RECORDS_DATABASE:
        if record["record_id"] == record_id:
            return record
    
    raise HTTPException(status_code=404, detail="Record not found")

@router.get("/api/medical-records/{record_id}/download")
async def download_medical_record(record_id: str):
    """Download medical record file"""
    
    for record in RECORDS_DATABASE:
        if record["record_id"] == record_id:
            file_path = record["file_path"]
            
            try:
                if USE_CLOUD:
                    file_content = storage.download_file(file_path)
                else:
                    local_path = os.path.join(CLOUD_STORAGE_PATH, file_path)
                    with open(local_path, "rb") as f:
                        file_content = f.read()
                
                # Return base64 encoded file
                return {
                    "record_id": record_id,
                    "file_name": record["file_name"],
                    "file_content": base64.b64encode(file_content).decode('utf-8'),
                    "content_type": "application/pdf"
                }
            except Exception as e:
                raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
    
    raise HTTPException(status_code=404, detail="Record not found")

@router.delete("/api/medical-records/{record_id}")
async def delete_medical_record(record_id: str):
    """Delete medical record from cloud storage"""
    
    global RECORDS_DATABASE
    
    for i, record in enumerate(RECORDS_DATABASE):
        if record["record_id"] == record_id:
            # Delete file from storage
            file_path = record["file_path"]
            
            try:
                if USE_CLOUD:
                    storage.delete_file(file_path)
                else:
                    local_path = os.path.join(CLOUD_STORAGE_PATH, file_path)
                    if os.path.exists(local_path):
                        os.remove(local_path)
            except Exception as e:
                print(f"Error deleting file: {e}")
            
            # Remove from database
            RECORDS_DATABASE.pop(i)
            
            return {
                "success": True,
                "message": "Medical record deleted successfully"
            }
    
    raise HTTPException(status_code=404, detail="Record not found")

@router.get("/api/medical-records/patient/{patient_id}/history")
async def get_patient_history(patient_id: str):
    """Get complete medical history for a patient"""
    
    patient_records = [r for r in RECORDS_DATABASE if r["patient_id"] == patient_id]
    
    if not patient_records:
        return {
            "patient_id": patient_id,
            "total_records": 0,
            "records": [],
            "timeline": []
        }
    
    # Sort by test date
    sorted_records = sorted(patient_records, key=lambda x: x["test_date"], reverse=True)
    
    # Create timeline
    timeline = []
    for record in sorted_records:
        timeline.append({
            "date": record["test_date"],
            "test_type": record["test_type"],
            "lab_name": record["lab_name"],
            "record_id": record["record_id"]
        })
    
    return {
        "patient_id": patient_id,
        "patient_name": patient_records[0]["patient_name"],
        "total_records": len(patient_records),
        "records": sorted_records,
        "timeline": timeline
    }

@router.get("/api/medical-records/search")
async def search_medical_records(
    test_type: Optional[str] = None,
    lab_name: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    """Search medical records by various criteria"""
    
    results = RECORDS_DATABASE.copy()
    
    if test_type:
        results = [r for r in results if test_type.lower() in r["test_type"].lower()]
    
    if lab_name:
        results = [r for r in results if lab_name.lower() in r["lab_name"].lower()]
    
    if date_from:
        results = [r for r in results if r["test_date"] >= date_from]
    
    if date_to:
        results = [r for r in results if r["test_date"] <= date_to]
    
    return {
        "total": len(results),
        "records": results
    }

def generate_ai_summary(test_type: str, file_name: str) -> str:
    """Generate AI summary for medical report"""
    
    summaries = {
        "blood test": "Complete Blood Count (CBC) analysis. Monitor for abnormal values in RBC, WBC, platelets, and hemoglobin levels.",
        "x-ray": "Radiological imaging report. Review for any abnormalities in bone structure, soft tissue, or organ positioning.",
        "mri": "Magnetic Resonance Imaging scan. Detailed soft tissue analysis for diagnostic purposes.",
        "ct scan": "Computed Tomography scan. Cross-sectional imaging for detailed internal examination.",
        "ecg": "Electrocardiogram report. Heart rhythm and electrical activity analysis.",
        "ultrasound": "Ultrasound imaging report. Real-time visualization of internal organs and blood flow.",
        "biopsy": "Tissue sample analysis. Pathological examination for cellular abnormalities.",
        "urine test": "Urinalysis report. Check for kidney function, infections, and metabolic conditions."
    }
    
    test_type_lower = test_type.lower()
    for key, summary in summaries.items():
        if key in test_type_lower or key in file_name.lower():
            return summary
    
    return "Medical diagnostic report. Review with healthcare provider for detailed interpretation."

def setup_medical_records_system(app):
    """Setup medical records system routes"""
    app.include_router(router)
