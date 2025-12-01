import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, Cell
} from "recharts";
import AlarmSystem from '../components/AlarmSystem';

export default function DoctorAgent({ embedded = false }) {
  const [graphData, setGraphData] = useState([]);
  const [historyData, setHistoryData] = useState([]);
  const [currentVitals, setCurrentVitals] = useState(null);

  useEffect(() => {
    const interval = setInterval(fetchVitals, 2000);
    fetchVitals(); // initial fetch
    return () => clearInterval(interval);
  }, []);

  // -------------------------------------------------
  // Fetch vitals from IngestAgent backend
  // -------------------------------------------------
  const fetchVitals = async () => {
    try {
      console.log("Fetching from Codespaces URL...");
      const API_URL = "http://localhost:8000";
      console.log("API URL:", API_URL);
      const res = await axios.get(`${API_URL}/ingest/latest`);
      const vitals = res.data.latest;

      if (!vitals || Object.keys(vitals).length === 0) {
        console.log("No vitals available yet");
        return;
      }

      // Add historical sample
      setHistoryData(prev => [
        ...prev.slice(-20),
        {
          time: new Date().toLocaleTimeString(),
          ...vitals
        }
      ]);

      // Threshold Deviation Logic
      const thresholds = {
        heart_rate: { low: 60, high: 100 },
        bp: { low: 90, high: 140 },
        spo2: { low: 95, high: 100 },
        glucose: { low: 70, high: 140 }
      };

      const chart = Object.keys(vitals).map(key => {
        const value = parseFloat(vitals[key]);
        const { low, high } = thresholds[key] || { low: 0, high: 100 };

        let deviation = 0;
        let status = "normal";
        
        if (value < low) {
          deviation = low - value;  // Positive deviation for low values
          status = "low";
        } else if (value > high) {
          deviation = value - high; // Positive deviation for high values  
          status = "high";
        } else {
          deviation = 0;
          status = "normal";
        }

        return {
          name: key.replace('_', ' ').toUpperCase(),
          value: Math.abs(deviation), // Always show positive values
          actualValue: value,
          status: status
        };
      });

      setGraphData(chart);
      setCurrentVitals(vitals);
    } catch (err) {
      console.error("Error fetching vitals:", err);
    }
  };

  const barColor = (status) => {
    if (status === "high") return "#e74c3c";  // Red
    if (status === "low") return "#f39c12";   // Orange
    return "#27ae60";                        // Green
  };

  const handleAlarmAcknowledge = (alarmId) => {
    console.log('Alarm acknowledged:', alarmId);
  };

  return (
    <div style={{ 
      padding: embedded ? "10px" : "20px", 
      height: embedded ? "100%" : "100vh", 
      width: "100%", 
      boxSizing: "border-box",
      background: embedded ? "transparent" : "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)",
      overflowY: "auto",
      display: "flex",
      flexDirection: "column"
    }}>
      {!embedded && (
        <AlarmSystem 
          vitals={currentVitals} 
          onAcknowledge={handleAlarmAcknowledge} 
        />
      )}
      {!embedded && (
        <div style={{ 
          position: 'absolute', 
          top: '20px', 
          right: '20px', 
          zIndex: 1000 
        }}>
          <Link 
            to="/" 
            style={{
              backgroundColor: '#6c757d',
              color: 'white',
              padding: '10px 20px',
              borderRadius: '8px',
              textDecoration: 'none',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.3s ease'
            }}
            onMouseOver={(e) => {
              e.target.style.backgroundColor = '#28a745';
              e.target.style.transform = 'translateY(-2px)';
            }}
            onMouseOut={(e) => {
              e.target.style.backgroundColor = '#6c757d';
              e.target.style.transform = 'translateY(0)';
            }}
          >
            ← Back to Dashboard
          </Link>
        </div>
      )}
      
      <h2 style={{ marginBottom: '20px' }}>Doctor Agent — Live Vitals Monitoring</h2>
      <p style={{ color: "#888", marginTop: 0, textAlign: "center", fontSize: "16px" }}>
        🏥 Real-time Patient Monitoring Dashboard
      </p>

      {/* ---------------- LINE CHART ---------------- */}
      <h3 style={{ marginTop: "20px", marginBottom: "15px", color: "#e9ecef" }}>Live Vitals Over Time</h3>
      <div style={{ width: "100%", height: embedded ? "350px" : "450px" }}>
        <ResponsiveContainer width="100%" height="100%">
        <LineChart data={historyData}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />

          <Line type="monotone" dataKey="heart_rate" name="Heart Rate" stroke="#e74c3c" strokeWidth={2} />
          <Line type="monotone" dataKey="bp" name="Blood Pressure" stroke="#3498db" strokeWidth={2} />
          <Line type="monotone" dataKey="spo2" name="SpO₂" stroke="#27ae60" strokeWidth={2} />
          <Line type="monotone" dataKey="glucose" name="Glucose" stroke="#9b59b6" strokeWidth={2} />
        </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}