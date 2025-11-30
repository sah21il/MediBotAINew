import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import DoctorAgent from "./DoctorAgent";

const API = "https://effective-happiness-4wrjgp4xpw5cpw-8000.app.github.dev";

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
          color: "🔥#9b59b6",
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
      border: "1px solid #ddd",
      padding: 20,
      borderRadius: 12,
      background: "#242424",
      boxShadow: "0px 2px 8px rgba(0,0,0,0.09)",
      transition: "0.2s",
    }}>
      <h3>{info.name}</h3>
      <p style={{ color: "#888", fontSize: "14px" }}>{info.desc}</p>
      <p><strong>Status:</strong> <span style={{color: "#27ae60"}}>Ready</span></p>

      <Link
        to={info.route}
        style={{
          marginTop: 15,
          display: "inline-block",
          padding: "10px 16px",
          background: info.color,
          color: "white",
          borderRadius: 8,
          textDecoration: "none",
          fontWeight: "bold"
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
    wsRef.current = new WebSocket("wss://effective-happiness-4wrjgp4xpw5cpw-8000.app.github.dev/ws/agents");
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
    <div style={{ padding: 24 }}>
      <header style={{ display: "flex", justifyContent: "space-between" }}>
        <h1>MediBot Dashboard</h1>
        <div>System: <b>Online</b></div>
      </header>

      <div
        style={{
          marginTop: 25,
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: 20,
        }}
      >
        {/* LEFT SIDE — HEALTH AGENT WITH GRAPHS */}
        <div style={{
          padding: 20,
          borderRadius: 16,
          border: "1px solid #ddd",
          background: "#242424",
          boxShadow: "0 3px 10px rgba(0,0,0,0.12)"
        }}>
          <h2>🏥 Health Agent - Live Monitoring</h2>
          <DoctorAgent embedded={true} />
          <Link
              to={`/doctor`}
              style={{
                marginTop: 12,
                display: "inline-block",
                padding: "12px 20px",
                background: "#27ae60",
                color: "white",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: "bold"
              }}
            >
              Open Full Monitor
          </Link>
        </div>

        {/* RIGHT SIDE — OTHER AGENTS */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr",
            gap: 20,
            height: "fit-content"
          }}
        >
          {otherAgents.map(a => (
            <SmallAgentCard key={a.agent_id} agent={a} />
          ))}
        </div>
      </div>
    </div>
  );
}
