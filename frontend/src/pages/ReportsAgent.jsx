import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import UploadModal from "../components/UploadModal";
import Notification, { ConfirmDialog } from "../components/Notification";

export default function ReportsAgent() {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadMetadata, setUploadMetadata] = useState({
    patientName: "",
    patientId: "",
    testType: "",
    labName: "",
    testDate: new Date().toISOString().split('T')[0],
    notes: ""
  });
  const [notification, setNotification] = useState({ message: '', type: '' });
  const [confirmDialog, setConfirmDialog] = useState({ show: false, reportId: null });


  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      console.log("Fetching reports from cloud...");
      const response = await axios.get("http://localhost:8000/api/medical-records/list");
      console.log("Cloud records received:", response.data);
      
      // Transform cloud records to report format
      const transformedReports = response.data.records.map(record => {
        const displayName = record.patient_name || record.file_name || 'Unknown Patient';
        const testType = record.test_type || 'Medical Report';
        return {
          id: record.record_id,
          name: `${displayName} (${testType})`,
          type: testType,
          date: record.test_date,
          patient_id: record.patient_id,
          status: "pending",
          data: record
        };
      });
      
      setReports(transformedReports);
    } catch (error) {
      console.error("Error fetching reports:", error);
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

  const uploadToCloud = async () => {
    if (!uploadFile || !uploadMetadata.patientName || !uploadMetadata.testType || !uploadMetadata.labName) {
      setNotification({ message: 'Please fill all required fields', type: 'warning' });
      return;
    }

    const formData = new FormData();
    formData.append("file", uploadFile);
    formData.append("patient_name", uploadMetadata.patientName);
    formData.append("patient_id", uploadMetadata.patientId || "");
    formData.append("test_type", uploadMetadata.testType);
    formData.append("lab_name", uploadMetadata.labName);
    formData.append("test_date", uploadMetadata.testDate);
    formData.append("notes", uploadMetadata.notes || "");

    console.log("=== UPLOAD DATA ===");
    console.log("Patient Name:", uploadMetadata.patientName);
    console.log("Test Type:", uploadMetadata.testType);
    console.log("Lab Name:", uploadMetadata.labName);
    console.log("Test Date:", uploadMetadata.testDate);
    console.log("===================");

    try {
      const response = await axios.post("http://localhost:8000/api/medical-records/upload", formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setNotification({ 
        message: `Report uploaded successfully! Record ID: ${response.data.record.record_id}`, 
        type: 'success' 
      });
      
      setShowUploadModal(false);
      setUploadFile(null);
      setUploadMetadata({
        patientName: "",
        patientId: "",
        testType: "",
        labName: "",
        testDate: new Date().toISOString().split('T')[0],
        notes: ""
      });
      fetchReports();
    } catch (error) {
      setNotification({ 
        message: 'Upload failed: ' + (error.response?.data?.detail || error.message), 
        type: 'error' 
      });
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

  const deleteReport = async (reportId, e) => {
    e.stopPropagation();
    setConfirmDialog({ show: true, reportId });
  };

  const confirmDelete = async () => {
    const reportId = confirmDialog.reportId;
    setConfirmDialog({ show: false, reportId: null });
    
    try {
      await axios.delete(`http://localhost:8000/api/medical-records/${reportId}`);
      setReports(reports.filter(r => r.id !== reportId));
      if (selectedReport?.id === reportId) {
        setSelectedReport(null);
        setAnalysis("");
      }
      setNotification({ message: 'Report deleted successfully!', type: 'success' });
    } catch (error) {
      setNotification({ 
        message: 'Delete failed: ' + (error.response?.data?.detail || error.message), 
        type: 'error' 
      });
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
              Centralized Cloud Medical Records
            </p>
          </div>
        </div>
        
        <Link 
          to="/" 
          style={{
            backgroundColor: '#6c757d',
            color: 'white',
            padding: '12px 24px',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 'bold',
            transition: 'all 0.3s ease'
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#27ae60'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#6c757d'}
        >
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
            <div style={{ display: "flex", gap: "10px" }}>
              <button
                onClick={() => setShowUploadModal(true)}
                style={{
                  padding: "10px 20px",
                  background: "linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)",
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  cursor: "pointer",
                  fontSize: "14px",
                  fontWeight: "bold"
                }}
              >
                📤 Upload New Report
              </button>
              <button
                onClick={fetchReports}
                style={{
                  padding: "10px 20px",
                  background: "linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%)",
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  cursor: "pointer",
                  fontSize: "14px",
                  fontWeight: "bold"
                }}
              >
                🔄 Refresh Cloud
              </button>
            </div>
          </div>

          <div style={{ maxHeight: "500px", overflowY: "auto" }}>
            {reports.length === 0 ? (
              <div style={{ textAlign: "center", padding: "40px", color: "#adb5bd" }}>
                <div style={{ fontSize: "48px", marginBottom: "20px" }}>☁️</div>
                <p>No reports in cloud storage yet.</p>
                <p style={{ fontSize: "14px", marginTop: "10px" }}>Click "View Cloud Reports" to fetch from centralized medical records.</p>
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
                onMouseOver={(e) => e.currentTarget.style.background = "rgba(255, 255, 255, 0.1)"}
                onMouseOut={(e) => e.currentTarget.style.background = "rgba(255, 255, 255, 0.05)"}
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
                  <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
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
                    <button
                      onClick={(e) => deleteReport(report.id, e)}
                      style={{
                        padding: "6px 12px",
                        background: "#e74c3c",
                        color: "white",
                        border: "none",
                        borderRadius: "6px",
                        cursor: "pointer",
                        fontSize: "12px",
                        fontWeight: "bold"
                      }}
                      onMouseOver={(e) => e.target.style.background = "#c0392b"}
                      onMouseOut={(e) => e.target.style.background = "#e74c3c"}
                    >
                      🗑️ Delete
                    </button>
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
                  
                  <div style={{ display: "flex", gap: "10px" }}>
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
                        flex: 1,
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
                      💬 Doctor Assistant
                    </button>
                    <button
                      onClick={() => {
                        // Store analysis for AI reminder suggestions
                        localStorage.setItem('reportForReminders', JSON.stringify({
                          patient: selectedReport.name,
                          type: selectedReport.type,
                          analysis: analysis,
                          date: selectedReport.date
                        }));
                        window.location.href = '/reminders';
                      }}
                      style={{
                        flex: 1,
                        padding: "15px",
                        background: "linear-gradient(135deg, #f39c12 0%, #e67e22 100%)",
                        color: "white",
                        border: "none",
                        borderRadius: "10px",
                        fontSize: "16px",
                        fontWeight: "bold",
                        cursor: "pointer",
                        transition: "all 0.3s ease"
                      }}
                      onMouseOver={(e) => e.target.style.transform = "scale(1.02)"}
                      onMouseOut={(e) => e.target.style.transform = "scale(1)"}
                    >
                      🧠 AI Smart Reminders
                    </button>
                  </div>
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

      <UploadModal
        show={showUploadModal}
        onClose={() => {
          setShowUploadModal(false);
          setUploadFile(null);
        }}
        onUpload={uploadToCloud}
        uploadFile={uploadFile}
        setUploadFile={setUploadFile}
        metadata={uploadMetadata}
        setMetadata={setUploadMetadata}
      />

      <Notification
        message={notification.message}
        type={notification.type}
        onClose={() => setNotification({ message: '', type: '' })}
      />

      {confirmDialog.show && (
        <ConfirmDialog
          message="Are you sure you want to delete this report? This action cannot be undone."
          onConfirm={confirmDelete}
          onCancel={() => setConfirmDialog({ show: false, reportId: null })}
        />
      )}
    </div>
  );
}