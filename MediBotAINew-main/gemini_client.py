import google.generativeai as genai
import os

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBvrtl0key-gen-lang-client-0084923736"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel('gemini-pro')

def get_gemini_response(prompt: str) -> str:
    """Get response from Gemini AI"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI temporarily unavailable: {str(e)}"

def get_medical_analysis(vitals: dict) -> str:
    """Analyze vital signs using Gemini"""
    prompt = f"""
    As a medical AI assistant, analyze these vital signs:
    - Heart Rate: {vitals.get('pulse', 'N/A')} bpm
    - Blood Pressure: {vitals.get('bp_sys', 'N/A')}/{vitals.get('bp_dia', 'N/A')} mmHg
    - SpO2: {vitals.get('spo2', 'N/A')}%
    - Temperature: {vitals.get('temp', 'N/A')}°C
    - Respiratory Rate: {vitals.get('resp_rate', 'N/A')} breaths/min
    
    Provide a brief medical assessment and recommendations.
    """
    return get_gemini_response(prompt)

def get_reminder_suggestions(reminder_type: str, title: str, description: str) -> str:
    """Get AI suggestions for reminders"""
    prompt = f"""
    As a healthcare AI, provide suggestions for this {reminder_type} reminder:
    Title: {title}
    Description: {description}
    
    Give practical tips for timing, adherence, and best practices.
    """
    return get_gemini_response(prompt)

def get_condition_reminders(condition: str) -> str:
    """Get AI recommendations for medical condition"""
    prompt = f"""
    As a medical AI, recommend essential reminders for someone with {condition}.
    Include medications, monitoring, lifestyle, and appointments.
    Format as a clear list with specific times and frequencies.
    """
    return get_gemini_response(prompt)