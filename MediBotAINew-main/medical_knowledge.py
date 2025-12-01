"""
Medical Knowledge Base for AI Doctor Assistant
Contains medical data, patterns, and responses for enhanced chat training
"""

MEDICAL_KNOWLEDGE = {
    "vital_signs": {
        "heart_rate": {
            "normal": {"min": 60, "max": 100, "unit": "bpm"},
            "bradycardia": {"threshold": 60, "causes": ["Athletic conditioning", "Medications", "Heart block", "Hypothyroidism"]},
            "tachycardia": {"threshold": 100, "causes": ["Fever", "Dehydration", "Anxiety", "Hyperthyroidism", "Arrhythmia"]},
            "critical": {"low": 40, "high": 150}
        },
        "blood_pressure": {
            "normal": {"systolic": {"min": 90, "max": 120}, "diastolic": {"min": 60, "max": 80}},
            "hypertension": {"stage1": {"sys": 130, "dia": 80}, "stage2": {"sys": 140, "dia": 90}},
            "hypotension": {"threshold": 90, "causes": ["Dehydration", "Blood loss", "Medications", "Sepsis"]},
            "crisis": {"systolic": 180, "diastolic": 120}
        },
        "spo2": {
            "normal": {"min": 95, "max": 100, "unit": "%"},
            "hypoxemia": {"mild": 90, "moderate": 85, "severe": 80},
            "causes": ["Pneumonia", "COPD", "Asthma", "Pulmonary embolism"]
        },
        "temperature": {
            "normal": {"min": 36.1, "max": 37.2, "unit": "°C"},
            "fever": {"low": 37.3, "moderate": 38.3, "high": 39.4},
            "hypothermia": {"threshold": 35.0}
        }
    },
    
    "symptoms": {
        "chest_pain": {
            "cardiac": ["Crushing", "Radiating to arm/jaw", "Shortness of breath", "Sweating"],
            "pulmonary": ["Sharp", "Worse with breathing", "Cough", "Fever"],
            "musculoskeletal": ["Tender to touch", "Worse with movement", "Localized"]
        },
        "shortness_of_breath": {
            "acute": ["Pulmonary embolism", "Pneumothorax", "Acute MI", "Asthma attack"],
            "chronic": ["COPD", "Heart failure", "Anemia", "Obesity"]
        },
        "dizziness": {
            "cardiovascular": ["Orthostatic hypotension", "Arrhythmia", "Dehydration"],
            "neurological": ["Vertigo", "Migraine", "Stroke", "Inner ear infection"]
        }
    },
    
    "medications": {
        "antihypertensives": {
            "ACE_inhibitors": ["Lisinopril", "Enalapril", "Captopril"],
            "beta_blockers": ["Metoprolol", "Atenolol", "Propranolol"],
            "diuretics": ["Hydrochlorothiazide", "Furosemide", "Spironolactone"]
        },
        "cardiac": {
            "antiarrhythmics": ["Amiodarone", "Lidocaine", "Digoxin"],
            "anticoagulants": ["Warfarin", "Heparin", "Rivaroxaban"]
        }
    },
    
    "emergency_protocols": {
        "cardiac_arrest": ["CPR", "Defibrillation", "Epinephrine", "Advanced airway"],
        "stroke": ["FAST assessment", "CT scan", "tPA consideration", "Blood pressure management"],
        "sepsis": ["Blood cultures", "Antibiotics", "Fluid resuscitation", "Vasopressors"]
    }
}

CONVERSATION_PATTERNS = {
    "greetings": [
        "Hello! I'm your AI medical assistant. How can I help with patient care today?",
        "Good day! I'm here to assist with medical analysis and clinical decisions.",
        "Hi there! Ready to help with patient monitoring and medical insights."
    ],
    
    "vital_analysis": [
        "Let me analyze these vital signs for clinical significance...",
        "Based on the current readings, here's my assessment:",
        "Reviewing the patient's vitals against normal parameters..."
    ],
    
    "recommendations": [
        "Based on clinical guidelines, I recommend:",
        "Consider the following interventions:",
        "My clinical assessment suggests:"
    ],
    
    "follow_up": [
        "Would you like me to explain any specific aspect?",
        "Do you need additional clinical recommendations?",
        "Is there anything else about this patient I can help with?"
    ]
}

CLINICAL_SCENARIOS = {
    "hypertensive_crisis": {
        "triggers": ["blood pressure", "hypertension", "crisis"],
        "response": """🚨 **HYPERTENSIVE CRISIS DETECTED**

**Immediate Actions Required:**
• Continuous BP monitoring
• IV access established
• Neurological assessment
• Consider nicardipine or clevidipine
• Target: Reduce BP by 10-20% in first hour

**Workup Needed:**
• ECG, chest X-ray
• Basic metabolic panel
• Urinalysis
• Fundoscopic exam

**Red Flags:** Altered mental status, chest pain, shortness of breath"""
    },
    
    "sepsis_screening": {
        "triggers": ["fever", "infection", "sepsis", "qsofa"],
        "response": """🦠 **SEPSIS SCREENING PROTOCOL**

**qSOFA Criteria:**
• Respiratory rate ≥22/min
• Altered mental status
• Systolic BP ≤100 mmHg

**SIRS Criteria:**
• Temperature >38°C or <36°C
• Heart rate >90 bpm
• Respiratory rate >20/min
• WBC >12,000 or <4,000

**Sepsis Bundle:**
• Blood cultures before antibiotics
• Broad-spectrum antibiotics within 1 hour
• Fluid resuscitation 30ml/kg
• Serial lactate measurements"""
    },
    
    "cardiac_monitoring": {
        "triggers": ["heart rate", "cardiac", "arrhythmia", "ecg"],
        "response": """❤️ **CARDIAC MONITORING ASSESSMENT**

**Rhythm Analysis:**
• Rate, rhythm, axis evaluation
• P-wave morphology and PR interval
• QRS width and morphology
• ST-segment and T-wave changes

**Critical Arrhythmias:**
• Ventricular tachycardia/fibrillation
• Complete heart block
• Atrial fibrillation with RVR
• Multifocal atrial tachycardia

**Monitoring Parameters:**
• Continuous telemetry
• 12-lead ECG if changes
• Electrolyte monitoring
• Medication review"""
    }
}

def get_medical_response(query, vitals=None):
    """Generate contextual medical responses based on query and vitals"""
    query_lower = query.lower()
    
    # Check for clinical scenarios
    for scenario, data in CLINICAL_SCENARIOS.items():
        if any(trigger in query_lower for trigger in data["triggers"]):
            return data["response"]
    
    # Vital signs analysis
    if vitals and any(word in query_lower for word in ["vital", "analyze", "assess"]):
        return analyze_vitals_comprehensive(vitals)
    
    # Medication queries
    if "medication" in query_lower or "drug" in query_lower:
        return get_medication_info(query_lower)
    
    # Symptom assessment
    if any(symptom in query_lower for symptom in ["pain", "shortness", "dizzy", "fever"]):
        return assess_symptoms(query_lower)
    
    return generate_general_response(query)

def analyze_vitals_comprehensive(vitals):
    """Comprehensive vital signs analysis"""
    analysis = "📊 **COMPREHENSIVE VITAL SIGNS ANALYSIS**\n\n"
    
    # Heart rate analysis
    hr = vitals.get('heart_rate', 0)
    if hr < 60:
        analysis += f"🔴 **Bradycardia**: HR {hr} bpm\n• Consider: Athletic conditioning, medications, heart block\n• Monitor for symptoms of decreased cardiac output\n\n"
    elif hr > 100:
        analysis += f"🟡 **Tachycardia**: HR {hr} bpm\n• Evaluate for: Fever, dehydration, anxiety, hyperthyroidism\n• Consider ECG if sustained\n\n"
    else:
        analysis += f"✅ **Heart Rate**: {hr} bpm (Normal)\n\n"
    
    # Blood pressure analysis
    bp = vitals.get('bp', 0)
    if bp > 140:
        analysis += f"🔴 **Hypertension**: {bp} mmHg\n• Stage 2 hypertension if confirmed\n• Consider antihypertensive therapy\n• Assess for target organ damage\n\n"
    elif bp < 90:
        analysis += f"🟡 **Hypotension**: {bp} mmHg\n• Evaluate for: Dehydration, blood loss, medications\n• Consider fluid resuscitation\n\n"
    else:
        analysis += f"✅ **Blood Pressure**: {bp} mmHg (Normal)\n\n"
    
    # SpO2 analysis
    spo2 = vitals.get('spo2', 0)
    if spo2 < 90:
        analysis += f"🔴 **Severe Hypoxemia**: {spo2}%\n• Immediate oxygen therapy required\n• Consider ABG analysis\n• Evaluate for respiratory failure\n\n"
    elif spo2 < 95:
        analysis += f"🟡 **Mild Hypoxemia**: {spo2}%\n• Supplemental oxygen may be needed\n• Monitor respiratory status\n\n"
    else:
        analysis += f"✅ **Oxygen Saturation**: {spo2}% (Normal)\n\n"
    
    analysis += "**Recommendations:**\n• Continue monitoring\n• Document trends\n• Notify physician of abnormal values\n• Consider additional diagnostics if indicated"
    
    return analysis

def get_medication_info(query):
    """Provide medication information"""
    if "blood pressure" in query or "hypertension" in query:
        return """💊 **ANTIHYPERTENSIVE MEDICATIONS**

**First-Line Agents:**
• **ACE Inhibitors**: Lisinopril, Enalapril
  - Mechanism: Block angiotensin conversion
  - Side effects: Dry cough, hyperkalemia
  
• **ARBs**: Losartan, Valsartan
  - Alternative to ACE inhibitors
  - Less likely to cause cough
  
• **Calcium Channel Blockers**: Amlodipine, Nifedipine
  - Vasodilation mechanism
  - Watch for peripheral edema
  
• **Diuretics**: HCTZ, Chlorthalidone
  - First-line for most patients
  - Monitor electrolytes

**Combination Therapy**: Often needed for BP control"""
    
    return "Please specify which medication or drug class you'd like information about."

def assess_symptoms(query):
    """Assess symptoms mentioned in query"""
    if "chest pain" in query:
        return """💔 **CHEST PAIN ASSESSMENT**

**Cardiac Causes:**
• Acute MI: Crushing, radiating pain
• Angina: Exertional, relieved by rest
• Pericarditis: Sharp, positional

**Pulmonary Causes:**
• PE: Sharp, with dyspnea
• Pneumonia: With fever, cough
• Pneumothorax: Sudden onset

**Assessment Tools:**
• HEART score for risk stratification
• ECG, troponins, chest X-ray
• Consider CT-PA if PE suspected"""
    
    if "shortness" in query or "dyspnea" in query:
        return """🫁 **DYSPNEA EVALUATION**

**Acute Causes:**
• Pulmonary embolism
• Pneumothorax
• Acute heart failure
• Asthma exacerbation

**Chronic Causes:**
• COPD
• Chronic heart failure
• Anemia
• Deconditioning

**Workup:**
• Chest X-ray, ABG
• BNP/NT-proBNP
• D-dimer if PE suspected
• Pulmonary function tests"""
    
    return "Please describe the specific symptoms you'd like me to assess."

def generate_general_response(query):
    """Generate general medical assistant response"""
    return f"""I understand you're asking about: "{query}"

As your AI medical assistant, I can help with:

🏥 **Clinical Analysis:**
• Vital signs interpretation
• Symptom assessment
• Risk stratification

💊 **Medication Information:**
• Drug interactions
• Dosing guidelines
• Side effects

📊 **Diagnostic Support:**
• Lab value interpretation
• Imaging findings
• Clinical decision tools

Could you be more specific about what medical information you need?"""