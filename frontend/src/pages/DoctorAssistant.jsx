import { useState, useEffect } from "react";
import axios from "axios";

export default function DoctorAssistant() {
  const [analysis, setAnalysis] = useState(null);
  const [vitals, setVitals] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const interval = setInterval(fetchAnalysis, 5000);
    fetchAnalysis(); // initial fetch
    return () => clearInterval(interval);
  }, []);

  const fetchAnalysis = async () => {
    try {
      setLoading(true);
      
      // Get latest vitals
      const vitalsRes = await axios.get("http://localhost:8000/ingest/latest");
      const currentVitals = vitalsRes.data.latest;
      
      if (!currentVitals || Object.keys(currentVitals).length === 0) {
        console.log("No vitals available for analysis");
        return;
      }
      
      setVitals(currentVitals);
      
      // Get medical analysis
      const analysisRes = await axios.post("http://localhost:8000/api/doctor-assistant/analyze", {
        vitals: currentVitals
      });
      
      setAnalysis(analysisRes.data.analysis);
      
    } catch (err) {
      console.error("Error fetching analysis:", err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    switch(level) {
      case "high": return "#e74c3c";
      case "medium": return "#f39c12"; 
      case "low": return "#27ae60";
      default: return "#95a5a6";
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case "critical": return "#e74c3c";
      case "concerning": return "#f39c12";
      case "stable": return "#27ae60";
      default: return "#95a5a6";
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "1200px", margin: "0 auto" }}>
      <h2>🤖 AI Doctor Assistant — Medical Analysis</h2>
      <p style={{ color: "#888", marginBottom: "20px" }}>
        <strong>Powered by Ollama LLM</strong> - Advanced AI medical analysis of vital signs
      </p>

      {loading && (
        <div style={{ textAlign: "center", padding: "20px", background: "#f8f9fa", borderRadius: "10px" }}>
          <div style={{ fontSize: "18px", marginBottom: "10px" }}>🧠 AI Analysis in Progress...</div>
          <div style={{ color: "#666" }}>Ollama is processing vital signs data</div>
        </div>
      )}

      {vitals && (
        <div style={{ 
          display: "grid", 
          gridTemplateColumns: "1fr 2fr", 
          gap: "20px",
          marginBottom: "20px"
        }}>
          {/* Current Vitals */}
          <div style={{
            background: "#f8f9fa",
            padding: "20px",
            borderRadius: "10px",
            border: "1px solid #dee2e6"
          }}>
            <h3>📊 Current Vitals</h3>
            <div style={{ display: "grid", gap: "10px" }}>
              <div><strong>Heart Rate:</strong> {vitals.heart_rate} bpm</div>
              <div><strong>Blood Pressure:</strong> {vitals.bp} mmHg</div>
              <div><strong>SpO₂:</strong> {vitals.spo2}%</div>
              <div><strong>Glucose:</strong> {vitals.glucose} mg/dL</div>
            </div>
          </div>

          {/* Overall Status */}
          {analysis && (
            <div style={{
              background: "#f8f9fa",
              padding: "20px", 
              borderRadius: "10px",
              border: "1px solid #dee2e6"
            }}>
              <h3>🎯 AI Assessment</h3>
              <div style={{ display: "grid", gap: "15px" }}>
                <div>
                  <strong>Status:</strong> 
                  <span style={{ 
                    color: getStatusColor(analysis.overall_status),
                    fontWeight: "bold",
                    marginLeft: "10px"
                  }}>
                    {analysis.overall_status.toUpperCase()}
                  </span>
                </div>
                <div>
                  <strong>Risk Level:</strong>
                  <span style={{ 
                    color: getRiskColor(analysis.risk_level),
                    fontWeight: "bold",
                    marginLeft: "10px"
                  }}>
                    {analysis.risk_level.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {analysis && (
        <div>
          <div style={{ 
            background: "#e8f5e8", 
            padding: "15px", 
            borderRadius: "8px", 
            marginBottom: "20px",
            border: "1px solid #c3e6cb"
          }}>
            <strong>🤖 AI Analysis:</strong> This assessment was generated using Ollama's advanced language model trained on medical knowledge.
          </div>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "20px" }}>
          
          {/* Medical Notes */}
          <div style={{
            background: "#fff3cd",
            padding: "20px",
            borderRadius: "10px", 
            border: "1px solid #ffeaa7"
          }}>
            <h3>📝 Medical Notes</h3>
            {analysis.medical_notes.length > 0 ? (
              <ul style={{ margin: 0, paddingLeft: "20px" }}>
                {analysis.medical_notes.map((note, index) => (
                  <li key={index} style={{ marginBottom: "8px" }}>{note}</li>
                ))}
              </ul>
            ) : (
              <p style={{ color: "#27ae60", fontStyle: "italic" }}>
                All vitals within normal parameters
              </p>
            )}
          </div>

          {/* Recommendations */}
          <div style={{
            background: "#d1ecf1", 
            padding: "20px",
            borderRadius: "10px",
            border: "1px solid #bee5eb"
          }}>
            <h3>💡 Recommendations</h3>
            {analysis.recommendations.length > 0 ? (
              <ul style={{ margin: 0, paddingLeft: "20px" }}>
                {analysis.recommendations.map((rec, index) => (
                  <li key={index} style={{ marginBottom: "8px" }}>{rec}</li>
                ))}
              </ul>
            ) : (
              <p style={{ color: "#27ae60", fontStyle: "italic" }}>
                Continue standard care protocols
              </p>
            )}
          </div>

          {/* Follow-up */}
          <div style={{
            background: "#d4edda",
            padding: "20px", 
            borderRadius: "10px",
            border: "1px solid #c3e6cb"
          }}>
            <h3>📅 Follow-up</h3>
            <ul style={{ margin: 0, paddingLeft: "20px" }}>
              {analysis.follow_up.map((item, index) => (
                <li key={index} style={{ marginBottom: "8px" }}>{item}</li>
              ))}
            </ul>
          </div>
          </div>
        </div>
      )}

      {!analysis && !loading && (
        <div style={{ 
          textAlign: "center", 
          padding: "40px",
          color: "#888"
        }}>
          Waiting for vital signs data to perform analysis...
        </div>
      )}
    </div>
  );
}