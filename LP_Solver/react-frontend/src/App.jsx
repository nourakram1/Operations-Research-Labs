import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import InputPage from "./InputPage";
import SolvePage from "./SolvePage";
import "./App.css";

export default function App() {
  return (
    <div className="app-container">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/input/:numVariables/:numConstraints" element={<InputPage />} />
          <Route path="/solve" element={<SolvePage />} />
        </Routes>
      </Router>
    </div>
  );
}
