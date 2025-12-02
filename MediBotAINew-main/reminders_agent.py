"""
Reminders Agent Backend - Smart Health & Medication Reminders with AI
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime, timedelta
import random
# from gemini_client import get_reminder_suggestions, get_condition_reminders

router = APIRouter()

# Mock reminders database - starts empty for clean demo
MOCK_REMINDERS = []

class ReminderCreate(BaseModel):
    type: str
    title: str
    description: str
    time: str
    frequency: str
    priority: str

class AISuggestionRequest(BaseModel):
    reminder_type: str
    title: str
    description: Optional[str] = ""

class AICreateRequest(BaseModel):
    medical_condition: str
    current_reminders: Optional[List[Dict]] = []

class AIBulkCreateRequest(BaseModel):
    medical_condition: str

@router.get("/api/reminders")
async def get_reminders():
    """Get all reminders"""
    # Sort by priority and next due time
    sorted_reminders = sorted(MOCK_REMINDERS, key=lambda x: (
        {"high": 0, "medium": 1, "low": 2}[x["priority"]],
        x["next_due"]
    ))
    return sorted_reminders

@router.post("/api/reminders")
async def create_reminder(reminder: ReminderCreate):
    """Create new reminder"""
    try:
        reminder_id = f"rem_{uuid.uuid4().hex[:6]}"
        
        # Calculate next due time
        now = datetime.now()
        time_parts = reminder.time.split(":")
        next_due = now.replace(
            hour=int(time_parts[0]), 
            minute=int(time_parts[1]), 
            second=0, 
            microsecond=0
        )
        
        # If time has passed today, schedule for tomorrow
        if next_due <= now:
            if reminder.frequency == "daily":
                next_due += timedelta(days=1)
            else:
                next_due += timedelta(days=1)
        
        new_reminder = {
            "id": reminder_id,
            "type": reminder.type,
            "title": reminder.title,
            "description": reminder.description,
            "time": reminder.time,
            "frequency": reminder.frequency,
            "priority": reminder.priority,
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "next_due": next_due.isoformat()
        }
        
        MOCK_REMINDERS.insert(0, new_reminder)
        
        return new_reminder
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating reminder: {str(e)}")

@router.delete("/api/reminders/{reminder_id}")
async def delete_reminder(reminder_id: str):
    """Delete reminder"""
    global MOCK_REMINDERS
    MOCK_REMINDERS = [r for r in MOCK_REMINDERS if r["id"] != reminder_id]
    return {"status": "deleted"}

@router.patch("/api/reminders/{reminder_id}/complete")
async def mark_reminder_complete(reminder_id: str):
    """Mark reminder as completed and schedule next occurrence"""
    for reminder in MOCK_REMINDERS:
        if reminder["id"] == reminder_id:
            now = datetime.now()
            time_parts = reminder["time"].split(":")
            
            # Schedule next occurrence based on frequency
            if reminder["frequency"] == "daily":
                next_due = now + timedelta(days=1)
                next_due = next_due.replace(hour=int(time_parts[0]), minute=int(time_parts[1]), second=0, microsecond=0)
                reminder["next_due"] = next_due.isoformat()
                reminder["status"] = "active"  # Keep active for recurring reminders
            elif reminder["frequency"] == "weekly":
                next_due = now + timedelta(weeks=1)
                next_due = next_due.replace(hour=int(time_parts[0]), minute=int(time_parts[1]), second=0, microsecond=0)
                reminder["next_due"] = next_due.isoformat()
                reminder["status"] = "active"
            elif reminder["frequency"] == "monthly":
                next_due = now + timedelta(days=30)
                next_due = next_due.replace(hour=int(time_parts[0]), minute=int(time_parts[1]), second=0, microsecond=0)
                reminder["next_due"] = next_due.isoformat()
                reminder["status"] = "active"
            else:
                # For as-needed, mark as completed and don't reschedule
                reminder["status"] = "completed"
                # Set next_due far in future so it doesn't trigger alarms
                reminder["next_due"] = (now + timedelta(days=365)).isoformat()
            
            return reminder
    
    raise HTTPException(status_code=404, detail="Reminder not found")

@router.post("/api/reminders/ai-suggestions")
async def get_ai_suggestions(request: AISuggestionRequest):
    """Get AI suggestions for reminders"""
    try:
        reminder_type = request.reminder_type
        title = request.title.lower()
        description = request.description.lower()
        
        suggestions = generate_ai_suggestions(reminder_type, title, description)
        
        return {
            "suggestions": suggestions,
            "confidence": 0.88,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI suggestion error: {str(e)}")

@router.post("/api/reminders/ai-create")
async def get_ai_reminder_recommendations(request: AICreateRequest):
    """Get AI recommendations for creating reminders based on medical condition"""
    try:
        condition = request.medical_condition.lower()
        report_analysis = request.dict().get('report_analysis', '')
        patient_name = request.dict().get('patient_name', '')
        current_reminders = request.current_reminders
        
        # Generate structured reminder suggestions
        suggestions = generate_structured_reminders(condition, report_analysis, current_reminders)
        
        return {
            "suggestions": suggestions,
            "condition": request.medical_condition,
            "patient_name": patient_name,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI recommendation error: {str(e)}")

@router.post("/api/reminders/ai-autocomplete")
async def ai_autocomplete_reminder(request: dict):
    """AI autocomplete for reminder details based on title"""
    try:
        title = request.get('title', '').lower()
        reminder_type = request.get('type', 'medication')
        condition = request.get('medical_condition', '').lower()
        
        result = generate_autocomplete_suggestions(title, reminder_type, condition)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI autocomplete error: {str(e)}")

@router.post("/api/reminders/ai-bulk-create")
async def create_ai_bulk_reminders(request: AIBulkCreateRequest):
    """Create multiple AI-recommended reminders based on medical condition"""
    try:
        condition = request.medical_condition.lower()
        ai_reminders = create_condition_based_reminders(condition)
        
        # Add to MOCK_REMINDERS
        for reminder in ai_reminders:
            MOCK_REMINDERS.insert(0, reminder)
        
        return {
            "reminders": ai_reminders,
            "count": len(ai_reminders),
            "condition": request.medical_condition
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI bulk create error: {str(e)}")

def generate_ai_suggestions(reminder_type: str, title: str, description: str) -> str:
    """Generate AI-powered suggestions for reminders"""
    
    if reminder_type == "medication":
        suggestions = "🤖 **AI MEDICATION SUGGESTIONS**\n\n"
        
        # Common medication patterns
        if "metformin" in title:
            suggestions += "**Metformin Optimization:**\n"
            suggestions += "• Take with meals to reduce GI side effects\n"
            suggestions += "• Best taken with breakfast and dinner\n"
            suggestions += "• Monitor blood glucose levels\n"
            suggestions += "• Stay hydrated throughout the day\n\n"
            suggestions += "**Timing Recommendations:**\n"
            suggestions += "• Morning: 8:00 AM with breakfast\n"
            suggestions += "• Evening: 6:00 PM with dinner\n"
            suggestions += "• Set phone alarms 15 minutes before meals\n\n"
        elif "insulin" in title:
            suggestions += "**Insulin Management:**\n"
            suggestions += "• Rotate injection sites to prevent lipodystrophy\n"
            suggestions += "• Check blood glucose before each dose\n"
            suggestions += "• Store properly (refrigerate unopened vials)\n"
            suggestions += "• Keep glucose tablets for hypoglycemia\n\n"
        elif "blood pressure" in title or "lisinopril" in title or "amlodipine" in title:
            suggestions += "**Blood Pressure Medication:**\n"
            suggestions += "• Take at same time daily for consistency\n"
            suggestions += "• Monitor BP weekly at home\n"
            suggestions += "• Avoid sudden position changes\n"
            suggestions += "• Limit sodium intake (<2300mg/day)\n\n"
        else:
            suggestions += "**General Medication Tips:**\n"
            suggestions += "• Set multiple alarms (phone, watch, pill dispenser)\n"
            suggestions += "• Use a weekly pill organizer\n"
            suggestions += "• Take with food if GI upset occurs\n"
            suggestions += "• Never skip doses without consulting doctor\n\n"
        
        suggestions += "**Smart Reminders:**\n"
        suggestions += "• Link to daily routines (brushing teeth, meals)\n"
        suggestions += "• Use medication tracking apps\n"
        suggestions += "• Set up pharmacy auto-refill\n"
        suggestions += "• Keep emergency supply when traveling"
        
    elif reminder_type == "appointment":
        suggestions = "🤖 **AI APPOINTMENT SUGGESTIONS**\n\n"
        
        if "cardiology" in title or "heart" in title:
            suggestions += "**Cardiology Appointment Prep:**\n"
            suggestions += "• Bring current medication list\n"
            suggestions += "• Record recent BP readings\n"
            suggestions += "• Note any chest pain or palpitations\n"
            suggestions += "• Bring previous ECGs or test results\n\n"
        elif "diabetes" in title or "endocrine" in title:
            suggestions += "**Diabetes Appointment Prep:**\n"
            suggestions += "• Bring glucose log (2 weeks minimum)\n"
            suggestions += "• List current medications and doses\n"
            suggestions += "• Note any hypoglycemic episodes\n"
            suggestions += "• Prepare questions about diet/exercise\n\n"
        else:
            suggestions += "**General Appointment Prep:**\n"
            suggestions += "• Arrive 15 minutes early\n"
            suggestions += "• Bring insurance card and ID\n"
            suggestions += "• List current symptoms or concerns\n"
            suggestions += "• Prepare questions for the doctor\n\n"
        
        suggestions += "**Smart Scheduling:**\n"
        suggestions += "• Book follow-up before leaving\n"
        suggestions += "• Set reminder 24 hours before\n"
        suggestions += "• Plan transportation in advance\n"
        suggestions += "• Block calendar for travel time"
        
    elif reminder_type == "exercise":
        suggestions = "🤖 **AI EXERCISE SUGGESTIONS**\n\n"
        
        suggestions += "**Optimal Exercise Timing:**\n"
        suggestions += "• Morning: Better consistency, metabolism boost\n"
        suggestions += "• Pre-meal: Can help with blood sugar control\n"
        suggestions += "• Avoid late evening: May affect sleep\n\n"
        
        if "walk" in title:
            suggestions += "**Walking Optimization:**\n"
            suggestions += "• Start with 10-15 minutes, gradually increase\n"
            suggestions += "• Aim for 150 minutes/week moderate activity\n"
            suggestions += "• Use step counter or fitness app\n"
            suggestions += "• Choose safe, well-lit routes\n\n"
        elif "gym" in title or "workout" in title:
            suggestions += "**Workout Planning:**\n"
            suggestions += "• Schedule 3-4 sessions per week\n"
            suggestions += "• Include rest days for recovery\n"
            suggestions += "• Mix cardio and strength training\n"
            suggestions += "• Stay hydrated before, during, after\n\n"
        
        suggestions += "**Motivation Tips:**\n"
        suggestions += "• Track progress with apps or journal\n"
        suggestions += "• Find exercise buddy for accountability\n"
        suggestions += "• Reward yourself for consistency\n"
        suggestions += "• Start small, build sustainable habits"
        
    elif reminder_type == "diet":
        suggestions = "🤖 **AI NUTRITION SUGGESTIONS**\n\n"
        
        suggestions += "**Meal Planning Tips:**\n"
        suggestions += "• Plan meals weekly to avoid impulsive choices\n"
        suggestions += "• Prep ingredients on weekends\n"
        suggestions += "• Keep healthy snacks readily available\n"
        suggestions += "• Use smaller plates for portion control\n\n"
        
        suggestions += "**Healthy Eating Patterns:**\n"
        suggestions += "• Include protein with each meal\n"
        suggestions += "• Fill half plate with vegetables\n"
        suggestions += "• Choose whole grains over refined\n"
        suggestions += "• Limit processed foods and added sugars\n\n"
        
        suggestions += "**Smart Reminders:**\n"
        suggestions += "• Set water intake reminders (8 glasses/day)\n"
        suggestions += "• Plan grocery shopping weekly\n"
        suggestions += "• Prep healthy snacks in advance\n"
        suggestions += "• Track food intake with apps if needed"
        
    elif reminder_type == "checkup":
        suggestions = "🤖 **AI HEALTH CHECKUP SUGGESTIONS**\n\n"
        
        suggestions += "**Preventive Care Schedule:**\n"
        suggestions += "• Annual physical exam\n"
        suggestions += "• Blood pressure check every 6 months\n"
        suggestions += "• Cholesterol screening every 5 years\n"
        suggestions += "• Diabetes screening every 3 years\n\n"
        
        suggestions += "**Age-Specific Screenings:**\n"
        suggestions += "• Mammogram: Annually after age 40\n"
        suggestions += "• Colonoscopy: Every 10 years after age 50\n"
        suggestions += "• Bone density: Every 2 years after age 65\n"
        suggestions += "• Eye exam: Annually after age 60\n\n"
        
        suggestions += "**Preparation Tips:**\n"
        suggestions += "• Fast 8-12 hours if blood work needed\n"
        suggestions += "• Bring list of current medications\n"
        suggestions += "• Note any new symptoms or concerns\n"
        suggestions += "• Update family medical history"
        
    else:
        suggestions = "🤖 **AI GENERAL SUGGESTIONS**\n\n"
        suggestions += "**Smart Reminder Strategies:**\n"
        suggestions += "• Use multiple reminder methods (phone, watch, notes)\n"
        suggestions += "• Link to existing habits for better compliance\n"
        suggestions += "• Set reminders 15 minutes before the actual time\n"
        suggestions += "• Use visual cues (sticky notes, pill organizers)\n\n"
        
        suggestions += "**Consistency Tips:**\n"
        suggestions += "• Same time daily builds stronger habits\n"
        suggestions += "• Track completion for motivation\n"
        suggestions += "• Adjust timing based on your schedule\n"
        suggestions += "• Have backup plans for busy days"
    
    return suggestions

def generate_condition_reminders(condition: str, current_reminders: List[Dict]) -> str:
    """Generate AI recommendations for reminders based on medical condition"""
    
    existing_types = [r.get('type', '') for r in current_reminders]
    existing_titles = [r.get('title', '').lower() for r in current_reminders]
    
    recommendations = f"🧠 **AI RECOMMENDATIONS FOR {condition.upper()}**\n\n"
    
    if "diabetes" in condition:
        recommendations += "**Essential Diabetes Management Reminders:**\n\n"
        
        if "medication" not in existing_types:
            recommendations += "💊 **Medication Reminders:**\n"
            recommendations += "• Metformin - 8:00 AM & 6:00 PM with meals\n"
            recommendations += "• Insulin (if prescribed) - Before meals\n\n"
        
        recommendations += "🩸 **Blood Sugar Monitoring:**\n"
        recommendations += "• Fasting glucose - 7:00 AM daily\n"
        recommendations += "• Post-meal glucose - 2 hours after meals\n\n"
        
        recommendations += "🏃 **Exercise & Diet:**\n"
        recommendations += "• 30-minute walk - 7:30 AM daily\n"
        recommendations += "• Meal planning - Sunday 6:00 PM\n\n"
        
        recommendations += "🏥 **Medical Appointments:**\n"
        recommendations += "• Endocrinologist visit - Every 3 months\n"
        recommendations += "• Eye exam - Every 6 months\n"
        recommendations += "• Foot check - Monthly\n"
        
    elif "hypertension" in condition or "blood pressure" in condition:
        recommendations += "**Essential Hypertension Management:**\n\n"
        
        recommendations += "💊 **Blood Pressure Medications:**\n"
        recommendations += "• ACE inhibitor - 8:00 AM daily\n"
        recommendations += "• Diuretic - 8:00 AM (if prescribed)\n\n"
        
        recommendations += "🩸 **BP Monitoring:**\n"
        recommendations += "• Morning BP check - 8:30 AM daily\n"
        recommendations += "• Evening BP check - 6:00 PM daily\n\n"
        
        recommendations += "🥗 **Lifestyle Reminders:**\n"
        recommendations += "• Low-sodium meal prep - Sunday 5:00 PM\n"
        recommendations += "• DASH diet planning - Weekly\n"
        recommendations += "• Limit alcohol - Daily reminder\n\n"
        
        recommendations += "🏃 **Exercise:**\n"
        recommendations += "• Cardio exercise - 7:00 AM, 5 days/week\n"
        recommendations += "• Stress reduction - 8:00 PM meditation\n"
        
    elif "heart" in condition or "cardiac" in condition:
        recommendations += "**Essential Cardiac Care Reminders:**\n\n"
        
        recommendations += "💊 **Heart Medications:**\n"
        recommendations += "• Beta-blocker - 8:00 AM & 8:00 PM\n"
        recommendations += "• Statin - 8:00 PM daily\n"
        recommendations += "• Aspirin - 8:00 AM daily (if prescribed)\n\n"
        
        recommendations += "🩸 **Monitoring:**\n"
        recommendations += "• Weight check - 7:00 AM daily\n"
        recommendations += "• Symptom tracking - Evening\n\n"
        
        recommendations += "🏃 **Cardiac Rehabilitation:**\n"
        recommendations += "• Gentle exercise - 9:00 AM daily\n"
        recommendations += "• Heart-healthy meal - Meal times\n\n"
        
        recommendations += "🏥 **Follow-ups:**\n"
        recommendations += "• Cardiologist visit - Every 3 months\n"
        recommendations += "• ECG/Echo - As scheduled\n"
        
    elif "asthma" in condition or "copd" in condition:
        recommendations += "**Essential Respiratory Care:**\n\n"
        
        recommendations += "💊 **Inhalers & Medications:**\n"
        recommendations += "• Controller inhaler - 8:00 AM & 8:00 PM\n"
        recommendations += "• Rescue inhaler - Keep accessible\n\n"
        
        recommendations += "🩸 **Monitoring:**\n"
        recommendations += "• Peak flow measurement - 8:00 AM daily\n"
        recommendations += "• Symptom tracking - Evening\n\n"
        
        recommendations += "🌬️ **Environmental:**\n"
        recommendations += "• Air quality check - 7:00 AM daily\n"
        recommendations += "• Trigger avoidance - Daily reminder\n"
        
    else:
        recommendations += "**General Health Management:**\n\n"
        recommendations += "💊 **Medication Adherence:**\n"
        recommendations += "• Morning medications - 8:00 AM\n"
        recommendations += "• Evening medications - 8:00 PM\n\n"
        
        recommendations += "🏥 **Regular Checkups:**\n"
        recommendations += "• Primary care visit - Every 6 months\n"
        recommendations += "• Specialist follow-up - As needed\n\n"
        
        recommendations += "🏃 **Wellness:**\n"
        recommendations += "• Daily exercise - 7:30 AM\n"
        recommendations += "• Healthy meal planning - Weekly\n"
    
    recommendations += "\n**Click 'Create These Reminders' to automatically add them to your schedule!**"
    return recommendations

def generate_autocomplete_suggestions(title: str, reminder_type: str, condition: str) -> Dict:
    """Generate AI suggestions for description, time, and priority based on title"""
    
    result = {
        "description": "",
        "time": "",
        "priority": "medium",
        "frequency": "daily"
    }
    
    # Medication-specific autocomplete
    if "metformin" in title:
        result["description"] = "Take 500mg with meals to reduce GI side effects. Monitor blood glucose levels."
        result["time"] = "08:00"
        result["priority"] = "high"
        result["frequency"] = "daily"
    elif "insulin" in title:
        result["description"] = "Check blood glucose before injection. Rotate injection sites. Keep glucose tablets handy."
        result["time"] = "07:30"
        result["priority"] = "high"
        result["frequency"] = "daily"
    elif "lisinopril" in title or "ace inhibitor" in title:
        result["description"] = "Blood pressure medication. Take at same time daily. Monitor for dizziness."
        result["time"] = "08:00"
        result["priority"] = "high"
        result["frequency"] = "daily"
    elif "amlodipine" in title or "calcium channel" in title:
        result["description"] = "BP medication. May cause ankle swelling. Take with or without food."
        result["time"] = "08:00"
        result["priority"] = "high"
        result["frequency"] = "daily"
    elif "aspirin" in title:
        result["description"] = "Take with food to prevent stomach upset. Low-dose for heart protection."
        result["time"] = "08:00"
        result["priority"] = "high"
        result["frequency"] = "daily"
    elif "statin" in title or "atorvastatin" in title or "simvastatin" in title:
        result["description"] = "Cholesterol medication. Take in evening for best effect. Report muscle pain."
        result["time"] = "20:00"
        result["priority"] = "high"
        result["frequency"] = "daily"
    elif "vitamin" in title:
        result["description"] = "Take with food for better absorption. Stay consistent with timing."
        result["time"] = "09:00"
        result["priority"] = "low"
        result["frequency"] = "daily"
    elif "blood sugar" in title or "glucose" in title:
        result["description"] = "Fasting blood glucose test. Record results in log. Target: 70-130 mg/dL."
        result["time"] = "07:00"
        result["priority"] = "high"
        result["frequency"] = "daily"
    elif "blood pressure" in title or "bp check" in title:
        result["description"] = "Sit quietly for 5 minutes before measuring. Record both readings."
        result["time"] = "08:30"
        result["priority"] = "high"
        result["frequency"] = "daily"
    elif "walk" in title or "walking" in title:
        result["description"] = "30-minute brisk walk. Wear comfortable shoes. Stay hydrated."
        result["time"] = "07:30"
        result["priority"] = "medium"
        result["frequency"] = "daily"
    elif "exercise" in title or "workout" in title:
        result["description"] = "Moderate intensity exercise. Warm up and cool down. Check BP if needed."
        result["time"] = "07:00"
        result["priority"] = "medium"
        result["frequency"] = "daily"
    elif "doctor" in title or "appointment" in title:
        result["description"] = "Bring medication list, insurance card, and list of questions. Arrive 15 min early."
        result["time"] = "09:00"
        result["priority"] = "high"
        result["frequency"] = "as-needed"
    elif "meal" in title or "diet" in title:
        result["description"] = "Healthy balanced meal. Include protein, vegetables, and whole grains."
        result["time"] = "12:00"
        result["priority"] = "medium"
        result["frequency"] = "daily"
    else:
        # Generic medication reminder
        if reminder_type == "medication":
            result["description"] = "Take as prescribed. Set alarm 15 minutes before. Don't skip doses."
            result["time"] = "08:00"
            result["priority"] = "high"
        elif reminder_type == "appointment":
            result["description"] = "Bring necessary documents. Arrive early. Prepare questions."
            result["time"] = "09:00"
            result["priority"] = "high"
        elif reminder_type == "exercise":
            result["description"] = "Stay active for better health. Start slow and build consistency."
            result["time"] = "07:30"
            result["priority"] = "medium"
        elif reminder_type == "checkup":
            result["description"] = "Regular health monitoring. Track results over time."
            result["time"] = "08:00"
            result["priority"] = "medium"
    
    return result

def generate_structured_reminders(condition: str, report_analysis: str, current_reminders: List[Dict]) -> List[Dict]:
    """Generate structured reminder suggestions with all details for checkbox selection"""
    
    suggestions = []
    
    if "diabetes" in condition or "glucose" in condition or "hba1c" in condition:
        suggestions.extend([
            {
                "type": "medication",
                "title": "Take Metformin 500mg",
                "description": "Take with breakfast to reduce GI side effects. Monitor blood glucose levels.",
                "time": "08:00",
                "frequency": "daily",
                "priority": "high",
                "reason": "Essential for blood sugar control in diabetes management"
            },
            {
                "type": "checkup",
                "title": "Check Fasting Blood Sugar",
                "description": "Test before breakfast. Target: 70-130 mg/dL. Record in log.",
                "time": "07:00",
                "frequency": "daily",
                "priority": "high",
                "reason": "Daily monitoring helps track diabetes control"
            },
            {
                "type": "checkup",
                "title": "Post-Meal Glucose Check",
                "description": "Test 2 hours after lunch. Target: <180 mg/dL.",
                "time": "14:00",
                "frequency": "daily",
                "priority": "medium",
                "reason": "Monitors how meals affect blood sugar"
            },
            {
                "type": "exercise",
                "title": "30-Minute Morning Walk",
                "description": "Brisk walk to improve insulin sensitivity. Wear comfortable shoes.",
                "time": "07:30",
                "frequency": "daily",
                "priority": "medium",
                "reason": "Exercise improves blood sugar control"
            },
            {
                "type": "diet",
                "title": "Healthy Meal Planning",
                "description": "Plan low-carb, high-fiber meals. Include vegetables and lean protein.",
                "time": "18:00",
                "frequency": "weekly",
                "priority": "medium",
                "reason": "Proper diet is crucial for diabetes management"
            },
            {
                "type": "appointment",
                "title": "Endocrinologist Follow-up",
                "description": "Bring glucose log and medication list. Discuss HbA1c results.",
                "time": "09:00",
                "frequency": "monthly",
                "priority": "high",
                "reason": "Regular monitoring by specialist"
            }
        ])
        
    elif "hypertension" in condition or "blood pressure" in condition or "bp" in condition:
        suggestions.extend([
            {
                "type": "medication",
                "title": "Take BP Medication (Lisinopril)",
                "description": "ACE inhibitor for blood pressure control. Take at same time daily.",
                "time": "08:00",
                "frequency": "daily",
                "priority": "high",
                "reason": "Critical for maintaining healthy blood pressure"
            },
            {
                "type": "checkup",
                "title": "Morning Blood Pressure Check",
                "description": "Sit quietly for 5 min before measuring. Target: <130/80 mmHg.",
                "time": "08:30",
                "frequency": "daily",
                "priority": "high",
                "reason": "Daily monitoring tracks treatment effectiveness"
            },
            {
                "type": "checkup",
                "title": "Evening Blood Pressure Check",
                "description": "Second daily reading. Record both systolic and diastolic.",
                "time": "18:00",
                "frequency": "daily",
                "priority": "medium",
                "reason": "Tracks BP variation throughout day"
            },
            {
                "type": "diet",
                "title": "Low-Sodium Meal Prep",
                "description": "DASH diet: <2300mg sodium/day. Use herbs instead of salt.",
                "time": "17:00",
                "frequency": "weekly",
                "priority": "high",
                "reason": "Low sodium diet reduces blood pressure"
            },
            {
                "type": "exercise",
                "title": "Cardio Exercise",
                "description": "30 min moderate activity. Walking, cycling, or swimming.",
                "time": "07:00",
                "frequency": "daily",
                "priority": "medium",
                "reason": "Regular exercise lowers blood pressure"
            }
        ])
        
    elif "cholesterol" in condition or "lipid" in condition or "ldl" in condition:
        suggestions.extend([
            {
                "type": "medication",
                "title": "Take Statin (Evening)",
                "description": "Atorvastatin or prescribed statin. Take in evening for best effect.",
                "time": "20:00",
                "frequency": "daily",
                "priority": "high",
                "reason": "Statins work best when taken at night"
            },
            {
                "type": "diet",
                "title": "Heart-Healthy Diet",
                "description": "Low saturated fat, high fiber. Include oats, nuts, fish.",
                "time": "12:00",
                "frequency": "daily",
                "priority": "high",
                "reason": "Diet significantly impacts cholesterol levels"
            },
            {
                "type": "exercise",
                "title": "Aerobic Exercise",
                "description": "45 min moderate intensity. Helps raise HDL (good cholesterol).",
                "time": "07:00",
                "frequency": "daily",
                "priority": "medium",
                "reason": "Exercise improves cholesterol profile"
            }
        ])
        
    elif "thyroid" in condition or "tsh" in condition:
        suggestions.extend([
            {
                "type": "medication",
                "title": "Take Thyroid Medication",
                "description": "Levothyroxine on empty stomach. Wait 30 min before eating.",
                "time": "06:30",
                "frequency": "daily",
                "priority": "high",
                "reason": "Must be taken on empty stomach for absorption"
            },
            {
                "type": "appointment",
                "title": "Thyroid Function Test",
                "description": "TSH blood test to monitor thyroid levels.",
                "time": "09:00",
                "frequency": "monthly",
                "priority": "medium",
                "reason": "Regular monitoring ensures proper dosing"
            }
        ])
        
    elif "vitamin" in condition or "deficiency" in condition:
        suggestions.extend([
            {
                "type": "medication",
                "title": "Take Vitamin D Supplement",
                "description": "1000 IU with breakfast for better absorption.",
                "time": "09:00",
                "frequency": "daily",
                "priority": "medium",
                "reason": "Corrects vitamin D deficiency"
            },
            {
                "type": "medication",
                "title": "Take B12 Supplement",
                "description": "Sublingual B12 or oral supplement.",
                "time": "09:00",
                "frequency": "daily",
                "priority": "medium",
                "reason": "Addresses B12 deficiency"
            }
        ])
        
    elif "anemia" in condition or "iron" in condition or "hemoglobin" in condition:
        suggestions.extend([
            {
                "type": "medication",
                "title": "Take Iron Supplement",
                "description": "Take with vitamin C for better absorption. Avoid with tea/coffee.",
                "time": "09:00",
                "frequency": "daily",
                "priority": "high",
                "reason": "Treats iron deficiency anemia"
            },
            {
                "type": "diet",
                "title": "Iron-Rich Foods",
                "description": "Include spinach, red meat, lentils, fortified cereals.",
                "time": "12:00",
                "frequency": "daily",
                "priority": "medium",
                "reason": "Dietary iron supports hemoglobin production"
            }
        ])
        
    else:
        # Generic health reminders
        suggestions.extend([
            {
                "type": "medication",
                "title": "Take Prescribed Medication",
                "description": "Follow doctor's instructions. Don't skip doses.",
                "time": "08:00",
                "frequency": "daily",
                "priority": "high",
                "reason": "Medication adherence is crucial for treatment"
            },
            {
                "type": "exercise",
                "title": "Daily Physical Activity",
                "description": "30 minutes of moderate exercise. Walking, yoga, or swimming.",
                "time": "07:30",
                "frequency": "daily",
                "priority": "medium",
                "reason": "Regular exercise improves overall health"
            },
            {
                "type": "appointment",
                "title": "Doctor Follow-up",
                "description": "Bring test results and medication list.",
                "time": "09:00",
                "frequency": "monthly",
                "priority": "high",
                "reason": "Regular monitoring by healthcare provider"
            }
        ])
    
    return suggestions

def create_condition_based_reminders(condition: str) -> List[Dict]:
    """Create actual reminder objects based on medical condition"""
    
    reminders = []
    now = datetime.now()
    
    if "diabetes" in condition:
        # Medication reminders
        reminders.extend([
            {
                "id": f"ai_{uuid.uuid4().hex[:6]}",
                "type": "medication",
                "title": "Take Metformin",
                "description": "500mg with breakfast",
                "time": "08:00",
                "frequency": "daily",
                "priority": "high",
                "status": "active",
                "created_at": now.strftime("%Y-%m-%d"),
                "next_due": (now + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0).isoformat()
            },
            {
                "id": f"ai_{uuid.uuid4().hex[:6]}",
                "type": "checkup",
                "title": "Check Blood Sugar",
                "description": "Fasting glucose test",
                "time": "07:00",
                "frequency": "daily",
                "priority": "high",
                "status": "active",
                "created_at": now.strftime("%Y-%m-%d"),
                "next_due": (now + timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0).isoformat()
            },
            {
                "id": f"ai_{uuid.uuid4().hex[:6]}",
                "type": "exercise",
                "title": "Morning Walk",
                "description": "30 minutes brisk walk for blood sugar control",
                "time": "07:30",
                "frequency": "daily",
                "priority": "medium",
                "status": "active",
                "created_at": now.strftime("%Y-%m-%d"),
                "next_due": (now + timedelta(days=1)).replace(hour=7, minute=30, second=0, microsecond=0).isoformat()
            }
        ])
        
    elif "hypertension" in condition or "blood pressure" in condition:
        reminders.extend([
            {
                "id": f"ai_{uuid.uuid4().hex[:6]}",
                "type": "medication",
                "title": "Take BP Medication",
                "description": "ACE inhibitor or prescribed BP med",
                "time": "08:00",
                "frequency": "daily",
                "priority": "high",
                "status": "active",
                "created_at": now.strftime("%Y-%m-%d"),
                "next_due": (now + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0).isoformat()
            },
            {
                "id": f"ai_{uuid.uuid4().hex[:6]}",
                "type": "checkup",
                "title": "Check Blood Pressure",
                "description": "Morning BP reading",
                "time": "08:30",
                "frequency": "daily",
                "priority": "high",
                "status": "active",
                "created_at": now.strftime("%Y-%m-%d"),
                "next_due": (now + timedelta(days=1)).replace(hour=8, minute=30, second=0, microsecond=0).isoformat()
            }
        ])
        
    elif "heart" in condition:
        reminders.extend([
            {
                "id": f"ai_{uuid.uuid4().hex[:6]}",
                "type": "medication",
                "title": "Take Heart Medication",
                "description": "Beta-blocker or prescribed cardiac med",
                "time": "08:00",
                "frequency": "daily",
                "priority": "high",
                "status": "active",
                "created_at": now.strftime("%Y-%m-%d"),
                "next_due": (now + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0).isoformat()
            },
            {
                "id": f"ai_{uuid.uuid4().hex[:6]}",
                "type": "checkup",
                "title": "Daily Weight Check",
                "description": "Monitor for fluid retention",
                "time": "07:00",
                "frequency": "daily",
                "priority": "medium",
                "status": "active",
                "created_at": now.strftime("%Y-%m-%d"),
                "next_due": (now + timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0).isoformat()
            }
        ])
    
    return reminders

# Add router to main FastAPI app
def setup_reminders_agent(app):
    app.include_router(router)