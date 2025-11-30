import React from "react";
import Dashboard from "./pages/Dashboard";
import DoctorAgent from "./pages/DoctorAgent";
import DoctorAssistant from "./pages/DoctorAssistant";
import { BrowserRouter, Routes, Route } from "react-router-dom";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/doctor" element={<DoctorAgent />} />
        <Route path="/doctor-assistant" element={<DoctorAssistant />} />
      </Routes>
    </BrowserRouter>
  );
}
