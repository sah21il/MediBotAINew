import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function DoctorAssistant() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hello! I'm your AI Doctor Assistant. I can help analyze patient vitals, answer medical questions, and provide clinical insights. How can I assist you today?",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [vitals, setVitals] = useState(null);
  const [analysisStatus, setAnalysisStatus] = useState("idle");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Fetch vitals every 10 seconds for analysis updates
    const interval = setInterval(fetchVitals, 10000);
    fetchVitals(); // initial fetch
    
    // Check for report data from Reports Agent (Discuss with AI)
    const reportData = localStorage.getItem('selectedReport');
    if (reportData) {
      const report = JSON.parse(reportData);
      const reportMessage = {
        id: Date.now(),
        type: 'bot',
        content: `📄 **Report Analysis Loaded**\n\n**Report:** ${report.name}\n**Type:** ${report.type}\n\n**AI Analysis:**\n${report.analysis}\n\nI'm ready to discuss this report with you. What would you like to know?`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, reportMessage]);
      localStorage.removeItem('selectedReport'); // Clear after use
    }
    
    // Check for doctor notification (Send to Doctor)
    const doctorNotification = localStorage.getItem('doctorNotification');
    if (doctorNotification) {
      const notification = JSON.parse(doctorNotification);
      const notificationMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: `📨 **New Report Analysis Received**\n\n**From:** Reports Agent\n**Report:** ${notification.report_name}\n**Type:** ${notification.report_type}\n**Patient:** ${notification.patient_id}\n**Time:** ${new Date(notification.timestamp).toLocaleString()}\n\n**Analysis Summary:**\n${notification.analysis.substring(0, 500)}...\n\n👩‍⚕️ **Doctor, please review this analysis and provide clinical guidance.**`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, notificationMessage]);
      localStorage.removeItem('doctorNotification'); // Clear after use
    }
    
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchVitals = async () => {
    try {
      const response = await axios.get("http://localhost:8000/ingest/latest");
      setVitals(response.data.latest);
      
      // Show analysis status update
      if (response.data.latest) {
        setAnalysisStatus("analyzing");
        setTimeout(() => setAnalysisStatus("complete"), 2000);
      }
    } catch (error) {
      console.error("Error fetching vitals:", error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    setIsTyping(true);

    try {
      // Simulate AI thinking time
      await new Promise(resolve => setTimeout(resolve, 1500));

      let botResponse = "";

      // Enhanced vital signs analysis and report discussion
      if (inputMessage.toLowerCase().includes('vital') || 
          inputMessage.toLowerCase().includes('patient') ||
          inputMessage.toLowerCase().includes('analyze') ||
          inputMessage.toLowerCase().includes('assess') ||
          inputMessage.toLowerCase().includes('report') ||
          inputMessage.toLowerCase().includes('findings')) {
        
        if (vitals) {
          const analysisRes = await axios.post("http://localhost:8000/api/doctor-assistant/analyze", {
            vitals: vitals
          });
          
          // Comprehensive vital analysis
          const hr = vitals.heart_rate;
          const bp = vitals.bp;
          const spo2 = vitals.spo2;
          const glucose = vitals.glucose;
          
          let clinicalAssessment = "";
          let alerts = [];
          
          // Heart rate assessment
          if (hr < 60) alerts.push(`🔴 Bradycardia: ${hr} bpm`);
          else if (hr > 100) alerts.push(`🟡 Tachycardia: ${hr} bpm`);
          
          // Blood pressure assessment
          if (bp > 140) alerts.push(`🔴 Hypertension: ${bp} mmHg`);
          else if (bp < 90) alerts.push(`🟡 Hypotension: ${bp} mmHg`);
          
          // Oxygen saturation
          if (spo2 < 90) alerts.push(`🔴 Severe Hypoxemia: ${spo2}%`);
          else if (spo2 < 95) alerts.push(`🟡 Mild Hypoxemia: ${spo2}%`);
          
          // Glucose assessment
          if (glucose > 180) alerts.push(`🟡 Hyperglycemia: ${glucose} mg/dL`);
          else if (glucose < 70) alerts.push(`🔴 Hypoglycemia: ${glucose} mg/dL`);
          
          clinicalAssessment = alerts.length > 0 ? 
            `\n⚠️ **Clinical Alerts:**\n${alerts.join('\n')}\n` : 
            "\n✅ **All parameters within normal limits**\n";
          
          botResponse = `📊 **COMPREHENSIVE VITAL SIGNS ANALYSIS**

**Current Readings:**
• Heart Rate: ${hr} bpm ${hr >= 60 && hr <= 100 ? '✅' : '⚠️'}
• Blood Pressure: ${bp} mmHg ${bp >= 90 && bp <= 140 ? '✅' : '⚠️'}
• SpO₂: ${spo2}% ${spo2 >= 95 ? '✅' : '⚠️'}
• Glucose: ${glucose} mg/dL ${glucose >= 70 && glucose <= 140 ? '✅' : '⚠️'}
${clinicalAssessment}
🤖 **AI Clinical Assessment:**
${analysisRes.data.analysis}

**Recommendations:**
• Continue monitoring trends
• Document any symptomatic changes
• Consider additional diagnostics if abnormal
• Notify physician of critical values

Would you like specific management recommendations for any abnormal values?`;
        } else {
          botResponse = "📊 **No Current Vital Signs Available**\n\nThe patient monitoring system appears to be offline or no recent data is available.\n\n**Troubleshooting Steps:**\n• Verify monitoring equipment connections\n• Check if sensors are properly attached\n• Ensure data transmission is active\n• Contact technical support if issues persist\n\n**I can still help with:**\n• Clinical protocols and guidelines\n• Medication information\n• Symptom assessment\n• Emergency procedures\n\nWhat would you like to know about?";
        }
      } else {
        // Enhanced medical assistant responses with better pattern matching
        botResponse = generateMedicalResponse(inputMessage);
      }

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: botResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: "I apologize, but I'm having trouble processing your request right now. Please try again or contact technical support.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const generateMedicalResponse = (input) => {
    const lowerInput = input.toLowerCase();
    
    // Greetings
    if (lowerInput.includes('hello') || lowerInput.includes('hi')) {
      const greetings = [
        "Hello! I'm your AI medical assistant. How can I help with patient care today?",
        "Hi there! Ready to assist with medical analysis and clinical decisions.",
        "Good day! I'm here to help with patient monitoring and medical insights."
      ];
      return greetings[Math.floor(Math.random() * greetings.length)];
    }
    
    // Help menu
    if (lowerInput.includes('help')) {
      return `🏥 **AI MEDICAL ASSISTANT CAPABILITIES**

**Patient Monitoring:**
• Real-time vital signs analysis
• Clinical parameter interpretation
• Risk stratification and alerts
• Trend analysis and predictions

**Clinical Decision Support:**
• Evidence-based recommendations
• Differential diagnosis assistance
• Treatment protocol guidance
• Drug interaction checking

**Emergency Protocols:**
• Sepsis screening (qSOFA, SIRS)
• Cardiac arrest algorithms
• Stroke assessment (FAST)
• Hypertensive crisis management

**Specialized Analysis:**
• ECG interpretation
• Lab value analysis
• Medication dosing
• Clinical calculations

**Example Queries:**
• "Analyze current patient vitals"
• "What causes elevated heart rate?"
• "Explain hypertension management"
• "Assess chest pain symptoms"
• "Check for drug interactions"`;
    }
    
    // Emergency protocols
    if (lowerInput.includes('emergency') || lowerInput.includes('critical')) {
      return "🚨 **EMERGENCY PROTOCOL REMINDER**\n\n**For life-threatening emergencies:**\n• Call 911 immediately\n• Begin CPR if no pulse\n• Use AED if available\n• Ensure airway patency\n\nI can assist with clinical protocols and decision support, but emergency situations require immediate human medical intervention.\n\n**How can I help with clinical analysis or protocols?**";
    }
    
    // Heart rate queries
    if (lowerInput.includes('heart rate') || lowerInput.includes('pulse') || lowerInput.includes('bradycardia') || lowerInput.includes('tachycardia')) {
      return `❤️ **HEART RATE ANALYSIS**

**Normal Range:** 60-100 bpm

**Bradycardia (<60 bpm):**
• Causes: Athletic conditioning, beta-blockers, heart block, hypothyroidism
• Symptoms: Fatigue, dizziness, syncope
• Treatment: Atropine, pacing if symptomatic

**Tachycardia (>100 bpm):**
• Causes: Fever, dehydration, anxiety, hyperthyroidism, arrhythmias
• Types: Sinus, SVT, VT, atrial fibrillation
• Management: Treat underlying cause, rate control

**Critical Values:**
• <40 bpm or >150 bpm require immediate attention
• Consider 12-lead ECG for rhythm analysis
• Monitor for hemodynamic instability`;
    }
    
    // Blood pressure queries - enhanced pattern matching
    if (lowerInput.includes('blood pressure') || lowerInput.includes('hypertension') || lowerInput.includes('hypotension') || 
        lowerInput.includes('bp') || /\d+\/\d+/.test(lowerInput) || lowerInput.includes('mmhg')) {
      return `🩸 **BLOOD PRESSURE MANAGEMENT**

**Classification:**
• Normal: <120/80 mmHg
• Elevated: 120-129/<80 mmHg
• Stage 1 HTN: 130-139/80-89 mmHg
• Stage 2 HTN: ≥140/90 mmHg
• Crisis: >180/120 mmHg

**Hypertensive Crisis Management:**
• Immediate BP reduction by 10-20%
• IV nicardipine or clevidipine
• Avoid sublingual nifedipine
• Monitor for end-organ damage

**Hypotension (<90 mmHg systolic):**
• Causes: Dehydration, blood loss, sepsis, medications
• Treatment: Fluid resuscitation, vasopressors
• Investigate underlying cause

**First-line Medications:**
• ACE inhibitors, ARBs, CCBs, thiazide diuretics`;
    }
    
    // Oxygen saturation
    if (lowerInput.includes('oxygen') || lowerInput.includes('spo2') || lowerInput.includes('hypoxemia')) {
      return `🫁 **OXYGEN SATURATION ASSESSMENT**

**Normal Range:** 95-100%

**Hypoxemia Classification:**
• Mild: 90-94%
• Moderate: 85-89%
• Severe: <85%

**Causes of Hypoxemia:**
• Pneumonia, COPD exacerbation
• Pulmonary embolism
• Asthma attack
• Pulmonary edema
• High altitude

**Management:**
• Supplemental oxygen therapy
• Target SpO2 94-98% (88-92% in COPD)
• Consider ABG analysis
• Evaluate for respiratory failure
• CPAP/BiPAP if indicated`;
    }
    
    // Chest pain
    if (lowerInput.includes('chest pain') || lowerInput.includes('angina')) {
      return `💔 **CHEST PAIN EVALUATION**

**Cardiac Causes:**
• **Acute MI:** Crushing, radiating to arm/jaw, diaphoresis
• **Unstable Angina:** Rest pain, crescendo pattern
• **Pericarditis:** Sharp, positional, friction rub

**Pulmonary Causes:**
• **PE:** Sharp, pleuritic, with dyspnea
• **Pneumothorax:** Sudden onset, unilateral
• **Pneumonia:** With fever, productive cough

**Assessment Tools:**
• **HEART Score:** Risk stratification
• **TIMI Score:** ACS risk assessment
• **Wells Score:** PE probability

**Immediate Workup:**
• 12-lead ECG, serial troponins
• Chest X-ray, D-dimer
• Consider CT-PA if PE suspected`;
    }
    
    // Medications
    if (lowerInput.includes('medication') || lowerInput.includes('drug')) {
      return `💊 **MEDICATION INFORMATION**

**Cardiovascular Medications:**
• **Beta-blockers:** Metoprolol, atenolol - reduce HR/BP
• **ACE inhibitors:** Lisinopril, enalapril - afterload reduction
• **Diuretics:** Furosemide, HCTZ - volume management
• **Anticoagulants:** Warfarin, heparin - clot prevention

**Drug Interactions:**
• Always check for contraindications
• Consider renal/hepatic function
• Monitor for adverse effects
• Adjust doses for elderly patients

**Common Side Effects:**
• ACE inhibitors: Dry cough, hyperkalemia
• Beta-blockers: Bradycardia, fatigue
• Diuretics: Hypokalemia, dehydration

**Specify medication name for detailed information**`;
    }
    
    // Sepsis
    if (lowerInput.includes('sepsis') || lowerInput.includes('infection') || lowerInput.includes('fever')) {
      return `🦠 **SEPSIS SCREENING & MANAGEMENT**

**qSOFA Criteria (≥2 = high risk):**
• Respiratory rate ≥22/min
• Altered mental status (GCS <15)
• Systolic BP ≤100 mmHg

**SIRS Criteria (≥2 = systemic response):**
• Temperature >38°C or <36°C
• Heart rate >90 bpm
• Respiratory rate >20/min
• WBC >12,000 or <4,000

**Sepsis-3 Hour Bundle:**
• Blood cultures before antibiotics
• Broad-spectrum antibiotics within 1 hour
• 30ml/kg crystalloid for hypotension
• Serial lactate measurements

**Severe Sepsis Indicators:**
• Organ dysfunction
• Hypotension despite fluids
• Lactate >2 mmol/L`;
    }
    
    // Check for specific BP values in question
    const bpMatch = input.match(/(\d+)\/(\d+)/);
    if (bpMatch) {
      const systolic = parseInt(bpMatch[1]);
      const diastolic = parseInt(bpMatch[2]);
      
      let assessment = "";
      let urgency = "";
      
      if (systolic >= 180 || diastolic >= 120) {
        urgency = "🚨 **HYPERTENSIVE CRISIS - IMMEDIATE ACTION REQUIRED**";
        assessment = `**Critical Hypertension: ${systolic}/${diastolic} mmHg**

${urgency}

**Immediate Management:**
• Continuous BP monitoring
• IV access and cardiac monitoring
• Reduce BP by 10-20% in first hour
• Consider IV nicardipine or clevidipine
• Assess for end-organ damage

**Workup Required:**
• 12-lead ECG
• Chest X-ray
• Basic metabolic panel
• Urinalysis
• Fundoscopic exam

**Complications to Monitor:**
• Acute stroke
• Acute MI
• Acute kidney injury
• Pulmonary edema

**DO NOT use sublingual nifedipine - can cause stroke!**`;
      } else if (systolic >= 140 || diastolic >= 90) {
        urgency = "⚠️ **STAGE 2 HYPERTENSION**";
        assessment = `**Hypertension: ${systolic}/${diastolic} mmHg**

${urgency}

**Assessment:**
• Confirm with repeat measurements
• Evaluate for target organ damage
• Consider secondary causes

**Management:**
• Lifestyle modifications
• Antihypertensive therapy indicated
• Goal: <130/80 mmHg for most patients

**First-line medications:**
• ACE inhibitors (lisinopril)
• ARBs (losartan)
• Calcium channel blockers (amlodipine)
• Thiazide diuretics (HCTZ)`;
      } else if (systolic >= 130 || diastolic >= 80) {
        urgency = "🟡 **STAGE 1 HYPERTENSION**";
        assessment = `**Elevated BP: ${systolic}/${diastolic} mmHg**

${urgency}

**10-year cardiovascular risk assessment needed**

**If risk ≥10%:**
• Start antihypertensive therapy
• Lifestyle modifications

**If risk <10%:**
• Lifestyle modifications first
• Recheck in 3-6 months

**Lifestyle changes:**
• DASH diet, sodium <2.3g/day
• Regular exercise
• Weight management
• Limit alcohol`;
      } else {
        assessment = `**Blood Pressure: ${systolic}/${diastolic} mmHg**

✅ **NORMAL BLOOD PRESSURE**

**Classification:**
• Normal: <120/80 mmHg
• Your reading is within normal limits

**Recommendations:**
• Continue healthy lifestyle
• Regular monitoring
• Maintain current habits`;
      }
      
      return assessment;
    }
    
    // Enhanced pattern matching for dangerous/critical terms
    if (lowerInput.includes('dangerous') || lowerInput.includes('critical') || lowerInput.includes('emergency')) {
      if (lowerInput.includes('bp') || lowerInput.includes('blood pressure')) {
        return `🚨 **DANGEROUS BLOOD PRESSURE LEVELS**

**Hypertensive Crisis (≥180/120 mmHg):**
• Life-threatening emergency
• Can cause stroke, heart attack, kidney failure
• Requires immediate medical intervention
• IV medications needed

**Severe Hypotension (<70 mmHg systolic):**
• Can cause organ failure
• May indicate shock
• Requires immediate fluid resuscitation
• Consider vasopressors

**Warning Signs:**
• Severe headache
• Chest pain
• Shortness of breath
• Neurological changes
• Altered mental status

**Call 911 immediately for BP crisis!**`;
      }
    }
    
    // General response with medical context
    return `I understand you're asking about: "${input}"

🏥 **Let me help with specific medical information:**

**For Blood Pressure Questions:**
• "Is 180/120 dangerous?" - Crisis assessment
• "Normal BP ranges" - Classification guide
• "Hypertension treatment" - Management options

**For Vital Signs:**
• "Heart rate 45 bpm" - Bradycardia evaluation
• "SpO2 88%" - Hypoxemia assessment
• "Temperature 39°C" - Fever management

**For Symptoms:**
• "Chest pain assessment" - Cardiac evaluation
• "Shortness of breath" - Respiratory causes
• "Dizziness causes" - Differential diagnosis

**Try being specific with your question for detailed clinical guidance!**`;
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div style={{
      height: "100vh",
      width: "100vw",
      background: "transparent",
      display: "flex",
      flexDirection: "column",
      overflow: "hidden",
      boxSizing: "border-box"
    }}>
      {/* Header */}
      <div style={{
        background: "rgba(45, 45, 45, 0.9)",
        padding: "15px 20px",
        borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "15px" }}>
          <div style={{
            width: "50px",
            height: "50px",
            background: "linear-gradient(135deg, #3498db 0%, #2ecc71 100%)",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "24px"
          }}>
            🤖
          </div>
          <div>
            <h2 style={{ margin: 0, color: "#e9ecef", fontSize: "24px" }}>
              AI Doctor Assistant
            </h2>
            <p style={{ margin: 0, color: "#adb5bd", fontSize: "14px" }}>
              Powered by Ollama LLM • {analysisStatus === "analyzing" ? "🔄 Analyzing..." : "🟢 Online"}
            </p>
          </div>
        </div>
        
        <Link 
          to="/" 
          style={{
            backgroundColor: '#6c757d',
            color: 'white',
            padding: '10px 20px',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 'bold',
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

      {/* Messages Area */}
      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        gap: "15px"
      }}>
        {messages.map((message) => (
          <div
            key={message.id}
            style={{
              display: "flex",
              justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
              alignItems: "flex-start",
              gap: "10px"
            }}
          >
            {message.type === 'bot' && (
              <div style={{
                width: "40px",
                height: "40px",
                background: "linear-gradient(135deg, #3498db 0%, #2ecc71 100%)",
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "18px",
                flexShrink: 0
              }}>
                🤖
              </div>
            )}
            
            <div style={{
              maxWidth: "70%",
              padding: "15px 20px",
              borderRadius: message.type === 'user' ? "20px 20px 5px 20px" : "20px 20px 20px 5px",
              background: message.type === 'user' 
                ? "linear-gradient(135deg, #3498db 0%, #2980b9 100%)"
                : "rgba(45, 45, 45, 0.9)",
              color: "#fff",
              border: message.type === 'bot' ? "1px solid rgba(255, 255, 255, 0.1)" : "none",
              whiteSpace: "pre-wrap",
              wordWrap: "break-word"
            }}>
              {message.content}
              <div style={{
                fontSize: "11px",
                opacity: 0.7,
                marginTop: "8px",
                textAlign: message.type === 'user' ? 'right' : 'left'
              }}>
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>

            {message.type === 'user' && (
              <div style={{
                width: "40px",
                height: "40px",
                background: "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)",
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "18px",
                flexShrink: 0
              }}>
                👨‍⚕️
              </div>
            )}
          </div>
        ))}

        {isTyping && (
          <div style={{
            display: "flex",
            alignItems: "center",
            gap: "10px"
          }}>
            <div style={{
              width: "40px",
              height: "40px",
              background: "linear-gradient(135deg, #3498db 0%, #2ecc71 100%)",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "18px"
            }}>
              🤖
            </div>
            <div style={{
              padding: "15px 20px",
              borderRadius: "20px 20px 20px 5px",
              background: "rgba(45, 45, 45, 0.9)",
              border: "1px solid rgba(255, 255, 255, 0.1)",
              color: "#adb5bd"
            }}>
              <div style={{ display: "flex", gap: "4px", alignItems: "center" }}>
                AI is thinking
                <span style={{ animation: "pulse 1.5s infinite" }}>●</span>
                <span style={{ animation: "pulse 1.5s infinite 0.5s" }}>●</span>
                <span style={{ animation: "pulse 1.5s infinite 1s" }}>●</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div style={{
        background: "rgba(45, 45, 45, 0.9)",
        padding: "20px",
        borderTop: "1px solid rgba(255, 255, 255, 0.1)"
      }}>
        <div style={{
          display: "flex",
          gap: "10px",
          alignItems: "flex-end"
        }}>
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about patient vitals, medical analysis, or clinical questions..."
            style={{
              flex: 1,
              minHeight: "50px",
              maxHeight: "120px",
              padding: "15px",
              borderRadius: "25px",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              background: "rgba(255, 255, 255, 0.1)",
              color: "#fff",
              fontSize: "16px",
              resize: "none",
              outline: "none"
            }}
            disabled={isTyping}
          />
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isTyping}
            style={{
              width: "50px",
              height: "50px",
              borderRadius: "50%",
              border: "none",
              background: inputMessage.trim() && !isTyping 
                ? "linear-gradient(135deg, #3498db 0%, #2ecc71 100%)"
                : "rgba(108, 117, 125, 0.5)",
              color: "#fff",
              fontSize: "20px",
              cursor: inputMessage.trim() && !isTyping ? "pointer" : "not-allowed",
              transition: "all 0.3s ease"
            }}
          >
            📤
          </button>
        </div>
      </div>

      <style jsx>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.4; }
          50% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}