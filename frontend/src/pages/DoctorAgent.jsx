import { useState, useEffect } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, Cell
} from "recharts";

export default function DoctorAgent() {
  const [graphData, setGraphData] = useState([]);
  const [historyData, setHistoryData] = useState([]);

  useEffect(() => {
    const interval = setInterval(fetchVitals, 3000);
    fetchVitals(); // initial fetch
    return () => clearInterval(interval);
  }, []);

  // -------------------------------------------------
  // Fetch vitals from IngestAgent backend
  // -------------------------------------------------
  const fetchVitals = async () => {
    try {
      const res = await axios.get("http://localhost:8000/ingest/latest");
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
    } catch (err) {
      console.error("Error fetching vitals:", err);
    }
  };

  const barColor = (status) => {
    if (status === "high") return "#e74c3c";  // Red
    if (status === "low") return "#f39c12";   // Orange
    return "#27ae60";                        // Green
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Doctor Agent — Live Vitals Monitoring</h2>
      <p style={{ color: "#888" }}>
        📡 Receiving data from external APIs every <b>3 seconds</b>...
      </p>
      
      {/* Debug info */}
      <div style={{ background: "#242424", padding: "10px", margin: "10px 0", borderRadius: "5px" }}>
        <strong>Current Vitals:</strong><br/>
        {graphData.map(item => (
          <div key={item.name}>
            {item.name}: {item.actualValue} (Deviation: {item.value}, Status: {item.status})
          </div>
        ))}
      </div>

      {/* ---------------- BAR CHART ---------------- */}
      <h3>Threshold Deviation Chart</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={graphData}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip formatter={(value, name, props) => [
            `Deviation: ${value}`, 
            `Actual: ${props.payload.actualValue}`
          ]} />
          <Legend />
          <Bar dataKey="value">
            {graphData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={barColor(entry.status)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      {/* ---------------- LINE CHART ---------------- */}
      <h3 style={{ marginTop: "40px" }}>Live Vitals Over Time</h3>
      <ResponsiveContainer width="100%" height={350}>
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
  );
}
