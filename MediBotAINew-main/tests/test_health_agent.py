import pytest
import json
from unittest.mock import Mock, patch
from agents.health_agent import HealthAgent

class TestHealthAgent:
    
    @pytest.fixture
    def health_agent(self):
        """Create a health agent instance for testing"""
        with patch('builtins.open', mock_open_medical_data()):
            agent = HealthAgent()
        return agent
    
    def test_normal_vitals(self, health_agent):
        """Test analysis of normal vital signs"""
        vitals = {
            "resp_rate": 18,
            "spo2": 98,
            "bp_sys": 120,
            "pulse": 75,
            "temp": 37.0,
            "consciousness": "Alert"
        }
        
        result = health_agent.analyze_vitals(vitals)
        assert "Normal Observation" in result or "normal" in result.lower()
    
    def test_critical_vitals(self, health_agent):
        """Test analysis of critical vital signs requiring MER call"""
        vitals = {
            "resp_rate": 35,
            "spo2": 85,
            "bp_sys": 200,
            "pulse": 150,
            "temp": 40.0,
            "consciousness": "Unresponsive"
        }
        
        result = health_agent.analyze_vitals(vitals)
        assert "MER Call" in result or "emergency" in result.lower()

def mock_open_medical_data():
    """Mock medical chart knowledge data"""
    medical_data = """
    Normal Vital Signs Ranges:
    - Respiratory Rate: 12-20 breaths/min
    - SpO2: 95-100%
    - Blood Pressure: 90-140 mmHg systolic
    - Heart Rate: 60-100 bpm
    - Temperature: 36.1-37.2°C
    """
    
    from unittest.mock import mock_open
    return mock_open(read_data=medical_data)