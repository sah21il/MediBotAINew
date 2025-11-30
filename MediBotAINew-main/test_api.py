#!/usr/bin/env python3
"""
Quick API test script
"""
import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing MediBot API...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Health check: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 2: Latest data
    try:
        response = requests.get(f"{base_url}/ingest/latest")
        print(f"✅ Latest data: {response.json()}")
    except Exception as e:
        print(f"❌ Latest data failed: {e}")
    
    # Test 3: Analyze vitals
    try:
        vitals = {
            "resp_rate": 20,
            "spo2": 95,
            "bp_sys": 130,
            "pulse": 80,
            "temp": 37.2,
            "consciousness": "Alert"
        }
        response = requests.post(f"{base_url}/api/health/analyze", json=vitals)
        print(f"✅ Analyze vitals: {response.json()}")
    except Exception as e:
        print(f"❌ Analyze vitals failed: {e}")

if __name__ == "__main__":
    test_api()