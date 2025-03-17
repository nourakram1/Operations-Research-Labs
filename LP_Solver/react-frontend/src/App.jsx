import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import InputPage from "./InputPage";
import SolvePage from "./SolvePage";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/input/:numVariables/:numConstraints/:numGoals" element={<InputPage />} />
        <Route path="/solve" element={<SolvePage />} />
      </Routes>
    </Router>
  );
}

export default App;
