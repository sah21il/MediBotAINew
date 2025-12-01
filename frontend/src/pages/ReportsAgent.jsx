import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function ReportsAgent() {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      console.log("Fetching reports...");
      const response = await axios.get("http://localhost:8000/api/reports");
      console.log("Reports received:", response.data);
      setReports(response.data);
    } catch (error) {
      console.error("Error fetching reports:", error);
      // Set empty array if error
      setReports([]);
    }
  };

  const analyzeReport = async (report) => {
    setLoading(true);
    setSelectedReport(report);
    
    // Update status to analyzed immediately in UI
    setReports(prevReports => 
      prevReports.map(r => 
        r.id === report.id ? { ...r, status: "analyzed" } : r
      )
    );
    
    try {
      const response = await axios.post("http://localhost:8000/api/reports/analyze", {
        report_id: report.id,
        report_type: report.type,
        data: report.data
      });
      setAnalysis(response.data.analysis);
      
      // Update the selected report status as well
      setSelectedReport(prev => ({ ...prev, status: "analyzed" }));
    } catch (error) {
      setAnalysis("Error analyzing report. Please try again.");
      // Revert status on error
      setReports(prevReports => 
        prevReports.map(r => 
          r.id === report.id ? { ...r, status: "pending" } : r
        )
      );
    }
    setLoading(false);
  };



  const uploadReport = async () => {
    if (!uploadFile) return;
    
    const formData = new FormData();
    formData.append("file", uploadFile);
    
    try {
      console.log("Uploading file:", uploadFile.name);
      const response = await axios.post("http://localhost:8000/api/reports/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log("Upload response:", response.data);
      setUploadFile(null);
      fetchReports();
      alert("Report uploaded successfully!");
    } catch (error) {
      console.error("Upload error:", error);
      alert("Error uploading report: " + (error.response?.data?.detail || error.message));
    }
  };

  const getReportIcon = (type) => {
    switch(type) {
      case "ECG": return "📈";
      case "X-Ray": return "🦴";
      case "Blood Test": return "🩸";
      case "MRI": return "🧠";
      case "CT Scan": return "💀";
      case "Ultrasound": return "👶";
      default: return "📄";
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case "analyzed": return "#27ae60";
      case "pending": return "#f39c12";
      case "critical": return "#e74c3c";
      default: return "#95a5a6";
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)",
      padding: "20px"
    }}>
      {/* Header */}
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "30px",
        padding: "20px",
        background: "rgba(45, 45, 45, 0.95)",
        borderRadius: "15px",
        border: "1px solid rgba(255, 255, 255, 0.1)"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "15px" }}>
          <div style={{
            width: "60px",
            height: "60px",
            background: "linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%)",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "28px"
          }}>
            📄
          </div>
          <div>
            <h1 style={{ margin: 0, color: "#e9ecef", fontSize: "32px" }}>
              Reports Agent
            </h1>
            <p style={{ margin: 0, color: "#adb5bd", fontSize: "16px" }}>
              Medical Report Analysis & Repository
            </p>
          </div>
        </div>
        
        <Link to="/" style={{
          backgroundColor: '#6c757d',
          color: 'white',
          padding: '12px 24px',
          borderRadius: '8px',
          textDecoration: 'none',
          fontWeight: 'bold'
        }}>
          ← Back to Dashboard
        </Link>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "30px" }}>
        {/* Reports Repository */}
        <div style={{
          background: "rgba(45, 45, 45, 0.95)",
          borderRadius: "15px",
          padding: "25px",
          border: "1px solid rgba(255, 255, 255, 0.1)"
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
            <h2 style={{ color: "#e9ecef", margin: 0 }}>📁 Reports Repository</h2>
            <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
              <input
                type="file"
                onChange={(e) => setUploadFile(e.target.files[0])}
                style={{ display: "none" }}
                id="file-upload"
                accept=".pdf,.jpg,.png,.dcm"
              />
              <label
                htmlFor="file-upload"
                style={{
                  padding: "8px 16px",
                  background: "#9b59b6",
                  color: "white",
                  borderRadius: "8px",
                  cursor: "pointer",
                  fontSize: "14px"
                }}
              >
                📤 Upload
              </label>
              {uploadFile && (
                <button
                  onClick={uploadReport}
                  style={{
                    padding: "8px 16px",
                    background: "#27ae60",
                    color: "white",
                    border: "none",
                    borderRadius: "8px",
                    cursor: "pointer"
                  }}
                >
                  Save
                </button>
              )}
            </div>
          </div>

          <div style={{ maxHeight: "500px", overflowY: "auto" }}>
            {reports.length === 0 ? (
              <div style={{ textAlign: "center", padding: "40px", color: "#adb5bd" }}>
                <div style={{ fontSize: "48px", marginBottom: "20px" }}>📄</div>
                <p>No reports found. Check if backend is running on port 8000.</p>
                <button 
                  onClick={fetchReports}
                  style={{
                    padding: "10px 20px",
                    background: "#9b59b6",
                    color: "white",
                    border: "none",
                    borderRadius: "8px",
                    cursor: "pointer",
                    marginTop: "10px"
                  }}
                >
                  🔄 Retry
                </button>
              </div>
            ) : (
              reports.map((report) => (
              <div
                key={report.id}
                onClick={() => analyzeReport(report)}
                style={{
                  padding: "15px",
                  margin: "10px 0",
                  background: "rgba(255, 255, 255, 0.05)",
                  borderRadius: "10px",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  cursor: "pointer",
                  transition: "all 0.3s ease"
                }}
                onMouseOver={(e) => e.target.style.background = "rgba(255, 255, 255, 0.1)"}
                onMouseOut={(e) => e.target.style.background = "rgba(255, 255, 255, 0.05)"}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <span style={{ fontSize: "24px" }}>{getReportIcon(report.type)}</span>
                    <div>
                      <h4 style={{ margin: 0, color: "#e9ecef" }}>{report.name}</h4>
                      <p style={{ margin: 0, color: "#adb5bd", fontSize: "12px" }}>
                        {report.type} • {report.date} • Patient: {report.patient_id}
                      </p>
                    </div>
                  </div>
                  <div style={{
                    padding: "4px 8px",
                    borderRadius: "12px",
                    background: getStatusColor(report.status),
                    color: "white",
                    fontSize: "10px",
                    fontWeight: "bold"
                  }}>
                    {report.status.toUpperCase()}
                  </div>
                </div>
              </div>
              ))
            )}
          </div>
        </div>

        {/* Analysis Panel */}
        <div style={{
          background: "rgba(45, 45, 45, 0.95)",
          borderRadius: "15px",
          padding: "25px",
          border: "1px solid rgba(255, 255, 255, 0.1)"
        }}>
          <h2 style={{ color: "#e9ecef", marginBottom: "20px" }}>🔍 Report Analysis</h2>
          
          {selectedReport ? (
            <div>
              <div style={{
                padding: "15px",
                background: "rgba(255, 255, 255, 0.05)",
                borderRadius: "10px",
                marginBottom: "20px"
              }}>
                <h3 style={{ color: "#e9ecef", margin: "0 0 10px 0" }}>
                  {getReportIcon(selectedReport.type)} {selectedReport.name}
                </h3>
                <p style={{ color: "#adb5bd", margin: 0, fontSize: "14px" }}>
                  Type: {selectedReport.type} | Date: {selectedReport.date} | Patient: {selectedReport.patient_id}
                </p>
              </div>

              {loading ? (
                <div style={{ textAlign: "center", padding: "40px", color: "#adb5bd" }}>
                  <div style={{ fontSize: "24px", marginBottom: "10px" }}>🔄</div>
                  Analyzing report...
                </div>
              ) : analysis ? (
                <div>
                  <div style={{
                    background: "rgba(39, 174, 96, 0.1)",
                    border: "1px solid rgba(39, 174, 96, 0.3)",
                    borderRadius: "10px",
                    padding: "20px",
                    marginBottom: "20px"
                  }}>
                    <h4 style={{ color: "#27ae60", margin: "0 0 15px 0" }}>🤖 AI Analysis Results</h4>
                    <div style={{ color: "#e9ecef", whiteSpace: "pre-wrap", lineHeight: "1.6" }}>
                      {analysis}
                    </div>
                  </div>
                  
                  <button
                    onClick={() => {
                      localStorage.setItem('selectedReport', JSON.stringify({
                        id: selectedReport.id,
                        name: selectedReport.name,
                        type: selectedReport.type,
                        analysis: analysis
                      }));
                      window.open('/doctor-assistant', '_blank');
                    }}
                    style={{
                      width: "100%",
                      padding: "15px",
                      background: "linear-gradient(135deg, #3498db 0%, #2980b9 100%)",
                      color: "white",
                      border: "none",
                      borderRadius: "10px",
                      fontSize: "16px",
                      fontWeight: "bold",
                      cursor: "pointer",
                      transition: "all 0.3s ease"
                    }}
                  >
                    💬 Send to Doctor Assistant
                  </button>
                </div>
              ) : null}
            </div>
          ) : (
            <div style={{ textAlign: "center", padding: "60px", color: "#adb5bd" }}>
              <div style={{ fontSize: "48px", marginBottom: "20px" }}>📄</div>
              <p>Select a report from the repository to analyze</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}