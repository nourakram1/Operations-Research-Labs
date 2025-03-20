import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, TextField, Card, CardContent } from "@mui/material";

function HomePage() {
  const navigate = useNavigate();
  const [numVariables, setNumVariables] = useState(2);
  const [numConstraints, setNumConstraints] = useState(1);
  const [numGoals, setNumGoals] = useState(0);

  const handleStart = () => {
    navigate(`/input/${numVariables}/${numConstraints}/${numGoals}`);
  };

  return (
    <Card sx={{ width: 1000, margin: "auto", padding: 2, textAlign: "center" }}>
      <CardContent>
        <h2>Linear Programming Solver</h2>
        <TextField label="Number of Variables" type="number" fullWidth margin="normal"
          value={numVariables} onChange={(e) => setNumVariables(Math.max(2, Number(e.target.value)))} 
          inputProps={{ min: 2 }} />
        <TextField label="Number of Constraints" type="number" fullWidth margin="normal"
          value={numConstraints} onChange={(e) => setNumConstraints(Math.max(1, Number(e.target.value)))} 
          inputProps={{ min: 1 }} />
        <TextField label="Number of Goals" type="number" fullWidth margin="normal"
          value={numGoals} onChange={(e) => setNumGoals(Math.max(0, Number(e.target.value)))} 
          inputProps={{ min: 0 }} />
        <Button variant="contained" color="primary" fullWidth sx={{ marginTop: 2 }} onClick={handleStart}>Start</Button>
      </CardContent>
    </Card>
  );
}

export default HomePage;