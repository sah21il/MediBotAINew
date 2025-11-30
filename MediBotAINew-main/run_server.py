#!/usr/bin/env python3
"""
MediBot Server Startup Script
Run this instead of main.py to avoid conflicts
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🏥 Starting MediBot AI Backend...")
    print("📊 Health monitoring system ready")
    print("🤖 AI Doctor Assistant enabled")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📱 Frontend should connect to: http://localhost:8000")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )