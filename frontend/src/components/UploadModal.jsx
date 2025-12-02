export default function UploadModal({ show, onClose, onUpload, uploadFile, setUploadFile, metadata, setMetadata }) {
  if (!show) return null;

  return (
    <div style={{
      position: "fixed",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: "rgba(0, 0, 0, 0.8)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 1000
    }}>
      <div style={{
        background: "#2d2d2d",
        borderRadius: "15px",
        padding: "30px",
        width: "500px",
        maxHeight: "80vh",
        overflowY: "auto"
      }}>
        <h2 style={{ color: "#e9ecef", marginBottom: "20px" }}>☁️ Upload to Cloud Medical Records</h2>
        
        <div style={{ marginBottom: "15px" }}>
          <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Select File *</label>
          <input
            type="file"
            onChange={(e) => setUploadFile(e.target.files[0])}
            accept=".pdf,.jpg,.png,.dcm"
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "8px",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              background: "rgba(255, 255, 255, 0.1)",
              color: "#fff"
            }}
          />
          {uploadFile && <p style={{ color: "#27ae60", fontSize: "12px", marginTop: "5px" }}>✓ {uploadFile.name}</p>}
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Patient Name *</label>
          <input
            type="text"
            value={metadata.patientName}
            onChange={(e) => setMetadata({...metadata, patientName: e.target.value})}
            placeholder="John Doe"
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "8px",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              background: "rgba(255, 255, 255, 0.1)",
              color: "#fff"
            }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Patient ID (Optional)</label>
          <input
            type="text"
            value={metadata.patientId}
            onChange={(e) => setMetadata({...metadata, patientId: e.target.value})}
            placeholder="Auto-generated if empty"
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "8px",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              background: "rgba(255, 255, 255, 0.1)",
              color: "#fff"
            }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Test Type *</label>
          <select
            value={metadata.testType}
            onChange={(e) => setMetadata({...metadata, testType: e.target.value})}
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "8px",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              background: "#2d2d2d",
              color: "#fff"
            }}
          >
            <option value="">Select test type</option>
            <option value="Blood Test">Blood Test</option>
            <option value="X-Ray">X-Ray</option>
            <option value="MRI">MRI</option>
            <option value="CT Scan">CT Scan</option>
            <option value="ECG">ECG</option>
            <option value="Ultrasound">Ultrasound</option>
            <option value="Biopsy">Biopsy</option>
            <option value="Urine Test">Urine Test</option>
          </select>
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Lab/Hospital Name *</label>
          <input
            type="text"
            value={metadata.labName}
            onChange={(e) => setMetadata({...metadata, labName: e.target.value})}
            placeholder="City Hospital Lab"
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "8px",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              background: "rgba(255, 255, 255, 0.1)",
              color: "#fff"
            }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Test Date *</label>
          <input
            type="date"
            value={metadata.testDate}
            onChange={(e) => setMetadata({...metadata, testDate: e.target.value})}
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "8px",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              background: "rgba(255, 255, 255, 0.1)",
              color: "#fff"
            }}
          />
        </div>

        <div style={{ marginBottom: "20px" }}>
          <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Notes (Optional)</label>
          <textarea
            value={metadata.notes}
            onChange={(e) => setMetadata({...metadata, notes: e.target.value})}
            placeholder="Additional notes..."
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "8px",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              background: "rgba(255, 255, 255, 0.1)",
              color: "#fff",
              minHeight: "60px",
              resize: "vertical"
            }}
          />
        </div>

        <div style={{ display: "flex", gap: "10px" }}>
          <button
            onClick={onUpload}
            disabled={!uploadFile || !metadata.patientName || !metadata.testType || !metadata.labName}
            style={{
              flex: 1,
              padding: "12px",
              background: uploadFile && metadata.patientName && metadata.testType && metadata.labName 
                ? "linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)" 
                : "#95a5a6",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontWeight: "bold",
              cursor: uploadFile && metadata.patientName && metadata.testType && metadata.labName ? "pointer" : "not-allowed"
            }}
          >
            ☁️ Upload to Cloud
          </button>
          <button
            onClick={onClose}
            style={{
              padding: "12px 20px",
              background: "#6c757d",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontWeight: "bold",
              cursor: "pointer"
            }}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
