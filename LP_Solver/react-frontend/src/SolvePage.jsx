import React from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, CardContent } from "@mui/material";

function SolvePage() {
  const navigate = useNavigate();
  
  return (
    <Card sx={{ maxWidth: 700, margin: "auto", padding: 2 }}>
      <CardContent>
        <h2>Step 3: Solution</h2>
        <p>Simplex tableau will be displayed here.</p>
        <Button variant="contained" color="primary" fullWidth sx={{ marginTop: 2 }} onClick={() => navigate("/")}>Start Over</Button>
      </CardContent>
    </Card>
  );
}

export default SolvePage;
