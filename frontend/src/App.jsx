import React from "react";
import Dashboard from "./pages/Dashboard";
import DoctorAgent from "./pages/DoctorAgent";
import DoctorAssistant from "./pages/DoctorAssistant";
import ReportsAgent from "./pages/ReportsAgent";
import RemindersAgent from "./pages/RemindersAgent";
import { BrowserRouter, Routes, Route } from "react-router-dom";

export default function App() {
  return (
    <div style={{
      width: "100vw",
      minHeight: "100vh",
      background: "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)"
    }}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/doctor" element={<DoctorAgent />} />
          <Route path="/doctor-assistant" element={<DoctorAssistant />} />
          <Route path="/reports" element={<ReportsAgent />} />
          <Route path="/reminders" element={<RemindersAgent />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}
