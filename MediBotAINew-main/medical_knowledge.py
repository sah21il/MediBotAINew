"""
Medical Knowledge Base - Provides specific medical information for accurate responses
"""

MEDICAL_KNOWLEDGE = {
    "vital_signs": {
        "heart_rate": {
            "normal": "60-100 bpm for adults at rest",
            "low": "Below 60 bpm (bradycardia) - may indicate heart block, hypothyroidism, or athletic conditioning",
            "high": "Above 100 bpm (tachycardia) - may indicate fever, anxiety, dehydration, or cardiac issues",
            "critical_low": "Below 40 bpm - requires immediate medical attention",
            "critical_high": "Above 140 bpm - requires immediate medical attention"
        },
        "blood_pressure": {
            "normal": "Systolic: 90-120 mmHg, Diastolic: 60-80 mmHg",
            "elevated": "Systolic: 120-129 mmHg - lifestyle changes recommended",
            "stage1_hypertension": "Systolic: 130-139 mmHg or Diastolic: 80-89 mmHg",
            "stage2_hypertension": "Systolic: ≥140 mmHg or Diastolic: ≥90 mmHg - medication required",
            "hypotension": "Below 90/60 mmHg - may cause dizziness, fainting",
            "crisis": "Above 180/120 mmHg - emergency medical care needed"
        },
        "spo2": {
            "normal": "95-100% oxygen saturation",
            "mild_hypoxemia": "90-94% - monitor closely, supplemental oxygen may be needed",
            "moderate_hypoxemia": "85-89% - supplemental oxygen required",
            "severe_hypoxemia": "Below 85% - emergency medical attention required"
        },
        "glucose": {
            "normal_fasting": "70-100 mg/dL",
            "prediabetes": "100-125 mg/dL fasting",
            "diabetes": "≥126 mg/dL fasting on two separate tests",
            "hypoglycemia": "Below 70 mg/dL - immediate glucose intake needed",
            "severe_hypoglycemia": "Below 54 mg/dL - emergency treatment required",
            "hyperglycemia": "Above 180 mg/dL - insulin or medication adjustment needed"
        },
        "temperature": {
            "normal": "36.5-37.5°C (97.7-99.5°F)",
            "low_grade_fever": "37.5-38.3°C (99.5-100.9°F)",
            "fever": "38.3-39.4°C (101-103°F) - antipyretics recommended",
            "high_fever": "Above 39.4°C (103°F) - medical evaluation needed",
            "hypothermia": "Below 35°C (95°F) - emergency care required"
        }
    },
    
    "common_conditions": {
        "hypertension": {
            "definition": "Chronic elevation of blood pressure ≥130/80 mmHg",
            "symptoms": "Often asymptomatic, may cause headaches, dizziness, blurred vision",
            "treatment": "Lifestyle modifications (diet, exercise, weight loss), ACE inhibitors, ARBs, diuretics, calcium channel blockers",
            "monitoring": "Home BP monitoring twice daily, medical checkup every 3-6 months"
        },
        "diabetes": {
            "definition": "Chronic condition with elevated blood glucose ≥126 mg/dL fasting",
            "symptoms": "Increased thirst, frequent urination, fatigue, blurred vision, slow wound healing",
            "treatment": "Type 1: Insulin therapy. Type 2: Metformin, lifestyle changes, possible insulin",
            "monitoring": "Daily glucose checks, HbA1c every 3 months, annual eye/foot exams"
        },
        "hypoxemia": {
            "definition": "Low oxygen levels in blood (SpO2 <95%)",
            "symptoms": "Shortness of breath, rapid breathing, confusion, bluish skin",
            "treatment": "Supplemental oxygen, treat underlying cause (pneumonia, COPD, heart failure)",
            "monitoring": "Continuous pulse oximetry, arterial blood gas if severe"
        }
    },
    
    "medications": {
        "metformin": {
            "class": "Biguanide antidiabetic",
            "indication": "Type 2 diabetes mellitus",
            "dosage": "500-2000 mg daily in divided doses with meals",
            "side_effects": "GI upset, diarrhea, lactic acidosis (rare)",
            "monitoring": "Renal function, vitamin B12 levels annually"
        },
        "lisinopril": {
            "class": "ACE inhibitor",
            "indication": "Hypertension, heart failure, post-MI",
            "dosage": "10-40 mg once daily",
            "side_effects": "Dry cough, hyperkalemia, angioedema (rare)",
            "monitoring": "BP, renal function, potassium levels"
        },
        "amlodipine": {
            "class": "Calcium channel blocker",
            "indication": "Hypertension, angina",
            "dosage": "5-10 mg once daily",
            "side_effects": "Peripheral edema, flushing, headache",
            "monitoring": "BP, heart rate, ankle swelling"
        }
    },
    
    "emergency_criteria": {
        "call_911": [
            "Chest pain or pressure lasting >5 minutes",
            "Difficulty breathing or severe shortness of breath",
            "Sudden severe headache with confusion",
            "Loss of consciousness or unresponsiveness",
            "Severe bleeding that won't stop",
            "Signs of stroke (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call 911)",
            "Blood pressure >180/120 mmHg with symptoms",
            "Blood glucose <54 mg/dL with altered mental status",
            "SpO2 <85% despite supplemental oxygen"
        ]
    }
}

def get_vital_assessment(vital_type: str, value: float) -> dict:
    """Get detailed assessment for a specific vital sign"""
    
    assessments = {
        "heart_rate": lambda v: {
            "status": "critical_low" if v < 40 else "low" if v < 60 else "normal" if v <= 100 else "high" if v <= 140 else "critical_high",
            "range": MEDICAL_KNOWLEDGE["vital_signs"]["heart_rate"]["normal"],
            "interpretation": MEDICAL_KNOWLEDGE["vital_signs"]["heart_rate"].get(
                "critical_low" if v < 40 else "low" if v < 60 else "normal" if v <= 100 else "high" if v <= 140 else "critical_high"
            )
        },
        "blood_pressure": lambda v: {
            "status": "hypotension" if v < 90 else "normal" if v <= 120 else "elevated" if v <= 129 else "stage1" if v <= 139 else "stage2" if v < 180 else "crisis",
            "range": MEDICAL_KNOWLEDGE["vital_signs"]["blood_pressure"]["normal"],
            "interpretation": MEDICAL_KNOWLEDGE["vital_signs"]["blood_pressure"].get(
                "hypotension" if v < 90 else "normal" if v <= 120 else "elevated" if v <= 129 else "stage1_hypertension" if v <= 139 else "stage2_hypertension" if v < 180 else "crisis"
            )
        },
        "spo2": lambda v: {
            "status": "severe" if v < 85 else "moderate" if v < 90 else "mild" if v < 95 else "normal",
            "range": MEDICAL_KNOWLEDGE["vital_signs"]["spo2"]["normal"],
            "interpretation": MEDICAL_KNOWLEDGE["vital_signs"]["spo2"].get(
                "severe_hypoxemia" if v < 85 else "moderate_hypoxemia" if v < 90 else "mild_hypoxemia" if v < 95 else "normal"
            )
        },
        "glucose": lambda v: {
            "status": "severe_low" if v < 54 else "low" if v < 70 else "normal" if v <= 100 else "prediabetes" if v <= 125 else "diabetes" if v <= 180 else "high",
            "range": MEDICAL_KNOWLEDGE["vital_signs"]["glucose"]["normal_fasting"],
            "interpretation": MEDICAL_KNOWLEDGE["vital_signs"]["glucose"].get(
                "severe_hypoglycemia" if v < 54 else "hypoglycemia" if v < 70 else "normal_fasting" if v <= 100 else "prediabetes" if v <= 125 else "diabetes" if v <= 180 else "hyperglycemia"
            )
        }
    }
    
    if vital_type in assessments:
        return assessments[vital_type](value)
    
    return {"status": "unknown", "range": "N/A", "interpretation": "Unable to assess"}

def get_condition_info(condition: str) -> dict:
    """Get detailed information about a medical condition"""
    condition_lower = condition.lower()
    
    for key, info in MEDICAL_KNOWLEDGE["common_conditions"].items():
        if key in condition_lower:
            return info
    
    return None

def get_medication_info(medication: str) -> dict:
    """Get detailed information about a medication"""
    med_lower = medication.lower()
    
    for key, info in MEDICAL_KNOWLEDGE["medications"].items():
        if key in med_lower:
            return info
    
    return None
