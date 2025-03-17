import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, TextField, Card, CardContent } from "@mui/material";

function Home() {
  const [numVariables, setNumVariables] = useState(2);
  const [numConstraints, setNumConstraints] = useState(2);
  const navigate = useNavigate();

  return (
    <Card sx={{ maxWidth: 500, margin: "auto", padding: 2 }}>
      <CardContent>
        <h2>Step 1: Choose Variables & Constraints</h2>
        <TextField label="Number of Variables" type="number" fullWidth value={numVariables} onChange={(e) => setNumVariables(Number(e.target.value))} />
        <TextField label="Number of Constraints" type="number" fullWidth value={numConstraints} onChange={(e) => setNumConstraints(Number(e.target.value))} sx={{ marginTop: 2 }} />
        <Button variant="contained" color="primary" fullWidth sx={{ marginTop: 2 }} onClick={() => navigate(`/input/${numVariables}/${numConstraints}`)}>Next</Button>
      </CardContent>
    </Card>
  );
}

export default Home;