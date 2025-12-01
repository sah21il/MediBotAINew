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
        current_reminders = request.current_reminders
        
        recommendations = generate_condition_reminders(condition, current_reminders)
        
        return {
            "recommendations": recommendations,
            "condition": request.medical_condition,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI recommendation error: {str(e)}")

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