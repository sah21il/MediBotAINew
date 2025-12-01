import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import DoctorAgent from "./DoctorAgent";

const API = "http://localhost:8000";

function SmallAgentCard({ agent }) {
  const getAgentInfo = (id) => {
    switch(id) {
      case "doctor_assistant":
        return {
          name: "🤖 Doctor Assistant",
          desc: "AI medical analysis and recommendations",
          color: "#3498db",
          route: "/doctor-assistant"
        };
      case "report":
        return {
          name: "📄 Report Agent", 
          desc: "Generate medical reports and summaries",
          color: "#9b59b6",
          route: "/reports"
        };
      case "reminder":
        return {
          name: "⏰ Reminder Agent",
          desc: "Medication and appointment reminders", 
          color: "#f39c12",
          route: "/reminders"
        };
      default:
        return {
          name: agent.agent_id.toUpperCase(),
          desc: "Medical assistant agent",
          color: "#95a5a6",
          route: `/agent/${agent.agent_id}`
        };
    }
  };
  
  const info = getAgentInfo(agent.agent_id);
  
  return (
    <div style={{
      border: "1px solid rgba(255, 255, 255, 0.1)",
      padding: "20px",
      borderRadius: "15px",
      background: "linear-gradient(135deg, #242424 0%, #2d2d2d 100%)",
      boxShadow: "0 8px 25px rgba(0,0,0,0.3)",
      transition: "all 0.3s ease",
      height: "100%",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      minHeight: "200px"
    }}>
      <div>
        <h3 style={{
          margin: "0 0 15px 0",
          color: "#e9ecef",
          fontSize: "18px",
          fontWeight: "bold"
        }}>{info.name}</h3>
        <p style={{ 
          color: "#adb5bd", 
          fontSize: "14px",
          margin: "0 0 15px 0",
          lineHeight: "1.4"
        }}>{info.desc}</p>
        <p style={{
          margin: "0 0 20px 0",
          fontSize: "14px"
        }}>
          <strong style={{ color: "#e9ecef" }}>Status:</strong> 
          <span style={{
            color: "#27ae60",
            marginLeft: "8px",
            fontWeight: "bold"
          }}>● Ready</span>
        </p>
      </div>

      <Link
        to={info.route}
        style={{
          display: "block",
          padding: "12px 20px",
          background: `linear-gradient(135deg, ${info.color} 0%, ${info.color}dd 100%)`,
          color: "white",
          borderRadius: "25px",
          textDecoration: "none",
          fontWeight: "bold",
          textAlign: "center",
          fontSize: "14px",
          boxShadow: `0 4px 15px ${info.color}40`,
          transition: "all 0.3s ease",
          textTransform: "uppercase",
          letterSpacing: "0.5px"
        }}
        onMouseOver={(e) => {
          e.target.style.transform = "translateY(-2px)";
          e.target.style.boxShadow = `0 6px 20px ${info.color}60`;
        }}
        onMouseOut={(e) => {
          e.target.style.transform = "translateY(0)";
          e.target.style.boxShadow = `0 4px 15px ${info.color}40`;
        }}
      >
        Open Agent
      </Link>
    </div>
  );
}

export default function Dashboard() {
  const [agents, setAgents] = useState([]);
  const wsRef = useRef(null);

  useEffect(() => {
    const load = async () => {
      const ids = ["health", "doctor_assistant", "report", "reminder"];
      const out = [];

      for (const id of ids) {
        try {
          const res = await axios.get(`${API}/agents/${id}/latest`);
          out.push(res.data ?? { agent_id: id });
        } catch {
          out.push({ agent_id: id });
        }
      }
      setAgents(out);
    };

    load();

    // WebSocket Updates
    wsRef.current = new WebSocket("ws://localhost:8000/ws/agents");
    wsRef.current.onmessage = (evt) => {
      const msg = JSON.parse(evt.data);

      if (msg.type === "agent_output") {
        setAgents((prev) => {
          const filtered = prev.filter((x) => x.agent_id !== msg.agent_id);
          return [msg, ...filtered];
        });
      }
    };

    return () => wsRef.current?.close();
  }, []);

  const healthAgent = agents.find(a => a.agent_id === "health");
  const otherAgents = agents.filter(a => a.agent_id !== "health");

  return (
    <div style={{ 
      padding: "15px", 
      minHeight: "100vh",
      width: "100vw",
      display: "flex",
      flexDirection: "column",
      boxSizing: "border-box",
      margin: 0,
      overflowY: "auto",
      overflowX: "hidden",
      background: "transparent",
      gap: "20px"
    }}>
      {/* Top Header */}
      <header style={{ 
        textAlign: "center", 
        padding: "25px 20px",
        background: "rgba(45, 45, 45, 0.95)",
        borderRadius: "20px",
        boxShadow: "0 8px 30px rgba(0,0,0,0.4)",
        flexShrink: 0,
        backdropFilter: "blur(15px)",
        border: "1px solid rgba(255, 255, 255, 0.15)",
        marginBottom: 0
      }}>
        <h1 style={{ 
          fontSize: "42px", 
          margin: "0 0 15px 0",
          color: "#ffffff",
          fontWeight: "900",
          letterSpacing: "2px",
          textShadow: "0 2px 10px rgba(0,0,0,0.5)"
        }}>
          🏥 MediBot AI Dashboard
        </h1>
        <p style={{ 
          fontSize: "20px", 
          color: "#e9ecef",
          margin: "0 0 25px 0",
          fontWeight: "500",
          opacity: "0.9"
        }}>
          Advanced Healthcare Monitoring & AI Analysis
        </p>
        <div style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: "20px",
          flexWrap: "wrap",
          width: "100%",
          maxWidth: "800px",
          margin: "0 auto"
        }}>
          <div style={{ 
            backgroundColor: "#28a745",
            color: "white",
            padding: "8px 15px",
            borderRadius: "20px",
            fontSize: "12px",
            fontWeight: "bold",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            boxShadow: "0 2px 10px rgba(40, 167, 69, 0.3)",
            whiteSpace: "nowrap"
          }}>
            <span style={{ fontSize: "16px" }}>🟢</span>
            System Online
          </div>
          <div style={{ 
            backgroundColor: "#17a2b8",
            color: "white",
            padding: "8px 15px",
            borderRadius: "20px",
            fontSize: "12px",
            fontWeight: "bold",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            boxShadow: "0 2px 10px rgba(23, 162, 184, 0.3)",
            whiteSpace: "nowrap"
          }}>
            <span style={{ fontSize: "16px" }}>🤖</span>
            AI Active
          </div>
          <div style={{ 
            backgroundColor: "#fd7e14",
            color: "white",
            padding: "8px 15px",
            borderRadius: "20px",
            fontSize: "12px",
            fontWeight: "bold",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            boxShadow: "0 2px 10px rgba(253, 126, 20, 0.3)",
            whiteSpace: "nowrap"
          }}>
            <span style={{ fontSize: "16px" }}>📊</span>
            Live Monitoring
          </div>
        </div>
      </header>

      {/* MAIN HEALTH MONITORING SECTION */}
      <div style={{
        padding: "25px",
        borderRadius: "20px",
        border: "2px solid #27ae60",
        background: "linear-gradient(135deg, #242424 0%, #2d2d2d 100%)",
        boxShadow: "0 12px 40px rgba(39, 174, 96, 0.25)",
        width: "100%",
        minHeight: "500px",
        boxSizing: "border-box",
        display: "flex",
        flexDirection: "column",
        marginBottom: 0
      }}>
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          marginBottom: "25px",
          gap: "15px",
          padding: "0 20px"
        }}>
          <div style={{
            width: "50px",
            height: "50px",
            backgroundColor: "#27ae60",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "24px"
          }}>
            📊
          </div>
          <h2 style={{
            fontSize: "28px",
            color: "#27ae60",
            margin: 0,
            fontWeight: "bold"
          }}>
            Live Patient Monitoring
          </h2>
          <div style={{
            width: "12px",
            height: "12px",
            backgroundColor: "#28a745",
            borderRadius: "50%",
            animation: "pulse 2s infinite"
          }}></div>
        </div>
        <div style={{ 
          flex: "1", 
          width: "100%",
          height: "100%",
          overflow: "hidden"
        }}>
          <DoctorAgent embedded={true} />
        </div>
        <div style={{ 
          textAlign: "center", 
          marginTop: "auto",
          padding: "25px",
          backgroundColor: "rgba(39, 174, 96, 0.15)",
          borderRadius: "15px",
          border: "1px solid rgba(39, 174, 96, 0.4)",
          backdropFilter: "blur(10px)"
        }}>
          <p style={{
            color: "#27ae60",
            margin: "0 0 15px 0",
            fontSize: "14px",
            fontWeight: "600"
          }}>
            🔍 Access detailed monitoring, alarms, and AI analysis
          </p>
          <Link
            to={`/doctor`}
            style={{
              display: "inline-block",
              padding: "15px 35px",
              background: "linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)",
              color: "white",
              borderRadius: 25,
              textDecoration: "none",
              fontWeight: "bold",
              fontSize: "16px",
              boxShadow: "0 6px 20px rgba(39, 174, 96, 0.4)",
              transition: "all 0.3s ease",
              textTransform: "uppercase",
              letterSpacing: "1px"
            }}
          >
            📊 Open Full Monitor
          </Link>
        </div>
      </div>

      {/* BOTTOM AGENTS SECTION */}
      <div style={{
        width: "100%",
        flexShrink: 0
      }}>
        <div style={{
          textAlign: "center",
          marginBottom: "30px",
          padding: "25px 20px",
          background: "rgba(45, 45, 45, 0.95)",
          borderRadius: "20px",
          boxShadow: "0 8px 30px rgba(0,0,0,0.4)",
          backdropFilter: "blur(15px)",
          border: "1px solid rgba(255, 255, 255, 0.15)"
        }}>
          <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "15px",
            marginBottom: "10px"
          }}>
            <div style={{
              width: "45px",
              height: "45px",
              backgroundColor: "#3498db",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "20px"
            }}>
              🤖
            </div>
            <h3 style={{
              fontSize: "24px",
              color: "#3498db",
              margin: 0,
              fontWeight: "bold"
            }}>
              AI Agent Services
            </h3>
          </div>
          <p style={{
            color: "#adb5bd",
            fontSize: "14px",
            margin: 0,
            fontStyle: "italic"
          }}>
            Specialized AI agents for comprehensive healthcare support
          </p>
        </div>
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "25px",
          width: "100%",
          boxSizing: "border-box",
          alignItems: "stretch"
        }}>
          {otherAgents.map(a => (
            <SmallAgentCard key={a.agent_id} agent={a} />
          ))}
        </div>
      </div>
    </div>
  );
}
