import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { LPProvider } from "./LPContext"; // Import Context Provider
import Home from "./Home";
import InputPage from "./InputPage";
import SolvePage from "./SolvePage";
import "./App.css";

function App() {
  return (
    <LPProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/input" element={<InputPage />} />
          <Route path="/solve" element={<SolvePage />} />
        </Routes>
      </Router>
    </LPProvider>
  );
}

export default App;
