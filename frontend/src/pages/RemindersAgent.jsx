import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function RemindersAgent() {
  const [reminders, setReminders] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newReminder, setNewReminder] = useState({
    type: "medication",
    title: "",
    description: "",
    time: "",
    frequency: "daily",
    priority: "medium"
  });
  const [aiSuggestions, setAiSuggestions] = useState("");
  const [loading, setLoading] = useState(false);
  const [medicalCondition, setMedicalCondition] = useState("");
  const [aiRecommendations, setAiRecommendations] = useState("");
  const [alarms, setAlarms] = useState([]);

  useEffect(() => {
    fetchReminders();
  }, []);

  const fetchReminders = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/reminders");
      setReminders(response.data);
    } catch (error) {
      console.error("Error fetching reminders:", error);
    }
  };

  const addReminder = async () => {
    if (!newReminder.title || !newReminder.time) return;
    
    try {
      const response = await axios.post("http://localhost:8000/api/reminders", newReminder);
      setReminders(prev => [response.data, ...prev]);
      setNewReminder({
        type: "medication",
        title: "",
        description: "",
        time: "",
        frequency: "daily",
        priority: "medium"
      });
      setShowAddForm(false);
    } catch (error) {
      alert("Error adding reminder");
    }
  };

  const deleteReminder = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/reminders/${id}`);
      setReminders(prev => prev.filter(r => r.id !== id));
    } catch (error) {
      alert("Error deleting reminder");
    }
  };

  const markComplete = async (id) => {
    try {
      console.log("Marking reminder complete:", id);
      const response = await axios.patch(`http://localhost:8000/api/reminders/${id}/complete`);
      console.log("Response:", response.data);
      
      // Update the reminder in the list
      setReminders(prev => prev.map(r => 
        r.id === id ? response.data : r
      ));
      
      // Also dismiss any active alarms for this reminder
      setAlarms(prev => prev.filter(a => a.reminder.id !== id));
      
    } catch (error) {
      console.error("Error updating reminder:", error);
      alert("Error updating reminder: " + (error.response?.data?.detail || error.message));
    }
  };

  const getAiSuggestions = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/api/reminders/ai-suggestions", {
        reminder_type: newReminder.type,
        title: newReminder.title,
        description: newReminder.description
      });
      setAiSuggestions(response.data.suggestions);
    } catch (error) {
      setAiSuggestions("Error getting AI suggestions");
    }
    setLoading(false);
  };

  const getAiRecommendations = async () => {
    if (!medicalCondition.trim()) {
      alert("Please enter a medical condition first");
      return;
    }
    
    setLoading(true);
    try {
      console.log("Getting AI recommendations for:", medicalCondition);
      const response = await axios.post("http://localhost:8000/api/reminders/ai-create", {
        medical_condition: medicalCondition,
        current_reminders: reminders.map(r => ({ type: r.type, title: r.title }))
      });
      console.log("AI recommendations response:", response.data);
      setAiRecommendations(response.data.recommendations);
    } catch (error) {
      console.error("Error getting AI recommendations:", error);
      setAiRecommendations("Error getting AI recommendations: " + (error.response?.data?.detail || error.message));
    }
    setLoading(false);
  };

  const createAiReminders = async () => {
    if (!medicalCondition.trim()) {
      alert("Please enter a medical condition first");
      return;
    }
    
    try {
      console.log("Sending request to create AI reminders...");
      const response = await axios.post("http://localhost:8000/api/reminders/ai-bulk-create", {
        medical_condition: medicalCondition
      });
      
      console.log("AI reminders response:", response.data);
      
      // Add all AI-created reminders to the list
      setReminders(prev => [...response.data.reminders, ...prev]);
      setAiRecommendations("");
      setMedicalCondition("");
      alert(`Created ${response.data.reminders.length} AI-recommended reminders!`);
    } catch (error) {
      console.error("Error creating AI reminders:", error);
      alert("Error creating AI reminders: " + (error.response?.data?.detail || error.message));
    }
  };

  const getReminderIcon = (type) => {
    switch(type) {
      case "medication": return "💊";
      case "appointment": return "🏥";
      case "exercise": return "🏃";
      case "diet": return "🥗";
      case "checkup": return "🩺";
      default: return "⏰";
    }
  };

  const getPriorityColor = (priority) => {
    switch(priority) {
      case "high": return "#e74c3c";
      case "medium": return "#f39c12";
      case "low": return "#27ae60";
      default: return "#95a5a6";
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case "completed": return "#27ae60";
      case "overdue": return "#e74c3c";
      case "pending": return "#f39c12";
      default: return "#3498db";
    }
  };

  const checkAlarm = (reminder) => {
    const now = new Date();
    const [hours, minutes] = reminder.time.split(':');
    const reminderTime = new Date();
    reminderTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
    
    // Trigger exactly at reminder time (within 10 second window)
    const timeDiff = now.getTime() - reminderTime.getTime();
    const isTimeMatch = timeDiff >= 0 && timeDiff <= 10000; // 0 to 10 seconds after
    const notAlreadyAlarmed = !alarms.some(a => a.reminder.id === reminder.id);
    
    if (isTimeMatch && reminder.status === "active" && notAlreadyAlarmed) {
      showAlarm(reminder);
    }
  };

  const showAlarm = (reminder) => {
    // Browser notification
    if (Notification.permission === "granted") {
      new Notification(`⏰ ${reminder.title}`, {
        body: reminder.description,
        icon: getReminderIcon(reminder.type)
      });
    }
    
    // Audio alarm
    const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT');
    audio.play().catch(() => {});
    
    // Visual alarm
    setAlarms(prev => [...prev, {
      id: Date.now(),
      reminder: reminder,
      timestamp: new Date()
    }]);
  };

  const dismissAlarm = (alarmId) => {
    setAlarms(prev => prev.filter(a => a.id !== alarmId));
  };

  // Request notification permission on load
  useEffect(() => {
    if (Notification.permission !== "granted" && Notification.permission !== "denied") {
      Notification.requestPermission();
    }
    
    // Check for due reminders every 5 seconds for precise timing
    const alarmInterval = setInterval(() => {
      reminders.forEach(reminder => {
        if (reminder.status === "active") {
          checkAlarm(reminder);
        }
      });
    }, 5000);
    
    return () => clearInterval(alarmInterval);
  }, [reminders]);

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
            background: "linear-gradient(135deg, #f39c12 0%, #e67e22 100%)",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "28px"
          }}>
            ⏰
          </div>
          <div>
            <h1 style={{ margin: 0, color: "#e9ecef", fontSize: "32px" }}>
              Smart Reminders Agent
            </h1>
            <p style={{ margin: 0, color: "#adb5bd", fontSize: "16px" }}>
              AI-Powered Health & Medication Reminders
            </p>
          </div>
        </div>
        
        <div style={{ display: "flex", gap: "10px" }}>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            style={{
              padding: "12px 24px",
              background: "linear-gradient(135deg, #f39c12 0%, #e67e22 100%)",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontWeight: "bold",
              cursor: "pointer"
            }}
          >
            ➕ Add Reminder
          </button>
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
      </div>

      <div style={{ display: "grid", gridTemplateColumns: showAddForm ? "1fr 1fr" : "1fr", gap: "30px" }}>
        {/* Reminders List */}
        <div style={{
          background: "rgba(45, 45, 45, 0.95)",
          borderRadius: "15px",
          padding: "25px",
          border: "1px solid rgba(255, 255, 255, 0.1)"
        }}>
          <h2 style={{ color: "#e9ecef", marginBottom: "20px" }}>📋 Active Reminders</h2>
          
          {reminders.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px", color: "#adb5bd" }}>
              <div style={{ fontSize: "48px", marginBottom: "20px" }}>⏰</div>
              <p>No reminders yet. Add your first reminder to get started!</p>
            </div>
          ) : (
            <div style={{ maxHeight: "600px", overflowY: "auto" }}>
              {reminders.map((reminder) => (
                <div
                  key={reminder.id}
                  style={{
                    padding: "20px",
                    margin: "15px 0",
                    background: "rgba(255, 255, 255, 0.05)",
                    borderRadius: "12px",
                    border: `2px solid ${getPriorityColor(reminder.priority)}`,
                    position: "relative"
                  }}

                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "10px" }}>
                        <span style={{ fontSize: "24px" }}>{getReminderIcon(reminder.type)}</span>
                        <h3 style={{ margin: 0, color: "#e9ecef" }}>{reminder.title}</h3>
                        <div style={{
                          padding: "4px 8px",
                          borderRadius: "12px",
                          background: getStatusColor(reminder.status),
                          color: "white",
                          fontSize: "10px",
                          fontWeight: "bold"
                        }}>
                          {reminder.status?.toUpperCase() || "ACTIVE"}
                        </div>
                      </div>
                      
                      <p style={{ color: "#adb5bd", margin: "0 0 10px 0", fontSize: "14px" }}>
                        {reminder.description}
                      </p>
                      
                      <div style={{ display: "flex", gap: "15px", fontSize: "12px", color: "#6c757d" }}>
                        <span>🕐 {reminder.time}</span>
                        <span>🔄 {reminder.frequency}</span>
                        <span>⚡ {reminder.priority} priority</span>
                      </div>
                    </div>
                    
                    <div style={{ display: "flex", gap: "8px" }}>
                      <button
                        onClick={() => {
                          console.log("Button clicked for reminder:", reminder.id);
                          markComplete(reminder.id);
                        }}
                        style={{
                          padding: "8px 12px",
                          background: reminder.status === "completed" ? "#95a5a6" : "#27ae60",
                          color: "white",
                          border: "none",
                          borderRadius: "6px",
                          fontSize: "12px",
                          cursor: "pointer"
                        }}
                      >
                        {reminder.status === "completed" ? "✅ Completed" : "✅ Done"}
                      </button>
                      <button
                        onClick={() => deleteReminder(reminder.id)}
                        style={{
                          padding: "8px 12px",
                          background: "#e74c3c",
                          color: "white",
                          border: "none",
                          borderRadius: "6px",
                          fontSize: "12px",
                          cursor: "pointer"
                        }}
                      >
                        🗑️ Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Add Reminder Form */}
        {showAddForm && (
          <div style={{
            background: "rgba(45, 45, 45, 0.95)",
            borderRadius: "15px",
            padding: "25px",
            border: "1px solid rgba(255, 255, 255, 0.1)"
          }}>
            <h2 style={{ color: "#e9ecef", marginBottom: "20px" }}>➕ Add New Reminder</h2>
            
            {/* Medical Condition Input */}
            <div style={{ marginBottom: "15px" }}>
              <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Medical Condition (Optional):</label>
              <input
                type="text"
                value={medicalCondition}
                onChange={(e) => setMedicalCondition(e.target.value)}
                placeholder="e.g., Diabetes, Hypertension, Heart Disease"
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
              <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Type:</label>
              <select
                value={newReminder.type}
                onChange={(e) => setNewReminder({...newReminder, type: e.target.value})}
                style={{
                  width: "100%",
                  padding: "10px",
                  borderRadius: "8px",
                  border: "1px solid rgba(255, 255, 255, 0.2)",
                  background: "#2d2d2d",
                  color: "#fff"
                }}
              >
                <option style={{ background: "#2d2d2d", color: "#fff" }} value="medication">💊 Medication</option>
                <option style={{ background: "#2d2d2d", color: "#fff" }} value="appointment">🏥 Appointment</option>
                <option style={{ background: "#2d2d2d", color: "#fff" }} value="exercise">🏃 Exercise</option>
                <option style={{ background: "#2d2d2d", color: "#fff" }} value="diet">🥗 Diet</option>
                <option style={{ background: "#2d2d2d", color: "#fff" }} value="checkup">🩺 Health Checkup</option>
                <option style={{ background: "#2d2d2d", color: "#fff" }} value="other">⏰ Other</option>
              </select>
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Title:</label>
              <input
                type="text"
                value={newReminder.title}
                onChange={(e) => setNewReminder({...newReminder, title: e.target.value})}
                placeholder="e.g., Take Metformin, Doctor Appointment"
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
              <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Description:</label>
              <textarea
                value={newReminder.description}
                onChange={(e) => setNewReminder({...newReminder, description: e.target.value})}
                placeholder="Additional details, dosage, location, etc."
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

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "15px", marginBottom: "15px" }}>
              <div>
                <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Time:</label>
                <input
                  type="time"
                  value={newReminder.time}
                  onChange={(e) => setNewReminder({...newReminder, time: e.target.value})}
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

              <div>
                <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Frequency:</label>
                <select
                  value={newReminder.frequency}
                  onChange={(e) => setNewReminder({...newReminder, frequency: e.target.value})}
                  style={{
                    width: "100%",
                    padding: "10px",
                    borderRadius: "8px",
                    border: "1px solid rgba(255, 255, 255, 0.2)",
                    background: "#2d2d2d",
                    color: "#fff"
                  }}
                >
                  <option style={{ background: "#2d2d2d", color: "#fff" }} value="daily">Daily</option>
                  <option style={{ background: "#2d2d2d", color: "#fff" }} value="weekly">Weekly</option>
                  <option style={{ background: "#2d2d2d", color: "#fff" }} value="monthly">Monthly</option>
                  <option style={{ background: "#2d2d2d", color: "#fff" }} value="as-needed">As Needed</option>
                </select>
              </div>
            </div>

            <div style={{ marginBottom: "20px" }}>
              <label style={{ color: "#e9ecef", display: "block", marginBottom: "5px" }}>Priority:</label>
              <select
                value={newReminder.priority}
                onChange={(e) => setNewReminder({...newReminder, priority: e.target.value})}
                style={{
                  width: "100%",
                  padding: "10px",
                  borderRadius: "8px",
                  border: "1px solid rgba(255, 255, 255, 0.2)",
                  background: "#2d2d2d",
                  color: "#fff"
                }}
              >
                <option style={{ background: "#2d2d2d", color: "#fff" }} value="low">🟢 Low Priority</option>
                <option style={{ background: "#2d2d2d", color: "#fff" }} value="medium">🟡 Medium Priority</option>
                <option style={{ background: "#2d2d2d", color: "#fff" }} value="high">🔴 High Priority</option>
              </select>
            </div>

            {/* AI Suggestions */}
            <div style={{ marginBottom: "20px" }}>
              <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
                <button
                  onClick={getAiSuggestions}
                  disabled={loading || !newReminder.title}
                  style={{
                    flex: 1,
                    padding: "8px 16px",
                    background: "linear-gradient(135deg, #3498db 0%, #2ecc71 100%)",
                    color: "white",
                    border: "none",
                    borderRadius: "6px",
                    fontSize: "12px",
                    cursor: "pointer",
                    opacity: loading || !newReminder.title ? 0.5 : 1
                  }}
                >
                  {loading ? "🔄 Getting Tips..." : "🤖 Get AI Tips"}
                </button>
                <button
                  onClick={getAiRecommendations}
                  disabled={loading || !medicalCondition}
                  style={{
                    flex: 1,
                    padding: "8px 16px",
                    background: "linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%)",
                    color: "white",
                    border: "none",
                    borderRadius: "6px",
                    fontSize: "12px",
                    cursor: "pointer",
                    opacity: loading || !medicalCondition ? 0.5 : 1
                  }}
                >
                  {loading ? "🔄 Creating..." : "🧠 AI Create Reminders"}
                </button>
              </div>
              
              {aiSuggestions && (
                <div style={{
                  padding: "15px",
                  background: "rgba(52, 152, 219, 0.1)",
                  border: "1px solid rgba(52, 152, 219, 0.3)",
                  borderRadius: "8px",
                  color: "#e9ecef",
                  fontSize: "14px",
                  whiteSpace: "pre-wrap",
                  marginBottom: "15px"
                }}>
                  <strong>🤖 AI Tips:</strong><br/>
                  {aiSuggestions}
                </div>
              )}
              
              {aiRecommendations && (
                <div style={{
                  padding: "15px",
                  background: "rgba(155, 89, 182, 0.1)",
                  border: "1px solid rgba(155, 89, 182, 0.3)",
                  borderRadius: "8px",
                  color: "#e9ecef",
                  fontSize: "14px",
                  whiteSpace: "pre-wrap",
                  marginBottom: "15px"
                }}>
                  <strong>🧠 AI Recommended Reminders:</strong><br/>
                  {aiRecommendations}
                  <div style={{ marginTop: "10px" }}>
                    <button
                      onClick={() => {
                        console.log("Creating AI reminders for:", medicalCondition);
                        createAiReminders();
                      }}
                      style={{
                        padding: "8px 16px",
                        background: "linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)",
                        color: "white",
                        border: "none",
                        borderRadius: "6px",
                        fontSize: "12px",
                        cursor: "pointer"
                      }}
                    >
                      ✅ Create These Reminders
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div style={{ display: "flex", gap: "10px" }}>
              <button
                onClick={addReminder}
                disabled={!newReminder.title || !newReminder.time}
                style={{
                  flex: 1,
                  padding: "12px",
                  background: "linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)",
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  fontWeight: "bold",
                  cursor: "pointer",
                  opacity: !newReminder.title || !newReminder.time ? 0.5 : 1
                }}
              >
                ✅ Add Reminder
              </button>
              <button
                onClick={() => setShowAddForm(false)}
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
                ❌ Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Alarm Notifications */}
      {alarms.map((alarm) => (
        <div
          key={alarm.id}
          style={{
            position: "fixed",
            top: "20px",
            right: "20px",
            background: "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)",
            color: "white",
            padding: "20px",
            borderRadius: "12px",
            boxShadow: "0 8px 25px rgba(231, 76, 60, 0.4)",
            zIndex: 9999,
            minWidth: "300px",
            animation: "pulse 2s infinite"
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "10px" }}>
                <span style={{ fontSize: "24px" }}>{getReminderIcon(alarm.reminder.type)}</span>
                <h3 style={{ margin: 0, fontSize: "18px" }}>⏰ REMINDER ALERT</h3>
              </div>
              <h4 style={{ margin: "0 0 5px 0", fontSize: "16px" }}>{alarm.reminder.title}</h4>
              <p style={{ margin: 0, fontSize: "14px", opacity: 0.9 }}>{alarm.reminder.description}</p>
              <p style={{ margin: "10px 0 0 0", fontSize: "12px", opacity: 0.8 }}>Time: {alarm.reminder.time}</p>
            </div>
            <button
              onClick={() => dismissAlarm(alarm.id)}
              style={{
                background: "rgba(255, 255, 255, 0.2)",
                border: "none",
                color: "white",
                borderRadius: "50%",
                width: "30px",
                height: "30px",
                cursor: "pointer",
                fontSize: "16px"
              }}
            >
              ✕
            </button>
          </div>
          <div style={{ marginTop: "15px", display: "flex", gap: "10px" }}>
            <button
              onClick={() => {
                markComplete(alarm.reminder.id);
                dismissAlarm(alarm.id);
              }}
              style={{
                flex: 1,
                padding: "8px",
                background: "rgba(255, 255, 255, 0.2)",
                border: "none",
                color: "white",
                borderRadius: "6px",
                cursor: "pointer",
                fontSize: "12px"
              }}
            >
              ✅ Mark Done
            </button>
            <button
              onClick={() => dismissAlarm(alarm.id)}
              style={{
                flex: 1,
                padding: "8px",
                background: "rgba(255, 255, 255, 0.2)",
                border: "none",
                color: "white",
                borderRadius: "6px",
                cursor: "pointer",
                fontSize: "12px"
              }}
            >
              ⏰ Snooze 5min
            </button>
          </div>
        </div>
      ))}

      <style jsx>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
      `}</style>
    </div>
  );
}