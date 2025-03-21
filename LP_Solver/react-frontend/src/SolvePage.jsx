import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button, Card, CardContent, Paper, Typography } from "@mui/material";
import SimplexTableau from "./SimplexTableau"; // Import the table component
import { InlineMath } from "react-katex";
import "katex/dist/katex.min.css";

function SolvePage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { result } = location.state || {};
  const [stepIndex, setStepIndex] = useState(0);

  if (!result || !result.steps) {
    return <p>No solution data available.</p>;
  }

  const step = result.steps[stepIndex];

  // Prepare data for SimplexTableau
  const simplexData = {
    variables: result.variables.concat("Solution"), // Header row
    basicVariables: step.zRows.concat(step.basicVariables), // First column (basic variables)
    tableau: step.simplexMatrix, // Matrix with first column
    enteringVariable: step.enteringVariable, // Column index for highlighting
    leavingVariable: step.leavingVariable, // Row index for highlighting
  };

  return (
    <Card sx={{ width: 1000, margin: "auto", padding: 3 }}>
      <CardContent>
        <h2>Solution</h2>

        {/* Comment Section */}
        <Typography 
          variant="subtitle1" 
          sx={{ backgroundColor: "#f0f0f0", padding: 2, borderRadius: 2, mb: 2 }}
        >
          <strong>Step {stepIndex + 1}:</strong> {step.comment} {/*<InlineMath>{step.comment}</InlineMath>*/}
        </Typography>

        {/* Simplex Tableau Component */}
        <Paper>
          <SimplexTableau data={simplexData} />
        </Paper>

        {/* Navigation Buttons */}
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: 10 }}>
          <Button 
            variant="contained" 
            color="secondary" 
            onClick={() => setStepIndex((prev) => Math.max(0, prev - 1))} 
            disabled={stepIndex === 0}
          >
            Previous
          </Button>
          <Button 
            variant="contained" 
            color="primary" 
            onClick={() => setStepIndex((prev) => Math.min(result.steps.length - 1, prev + 1))} 
            disabled={stepIndex === result.steps.length - 1}
          >
            Next
          </Button>
        </div>

        {/* Show Final Solution Button */}
        <Button 
          variant="contained" 
          color="success" 
          fullWidth 
          sx={{ marginTop: 2 }} 
          onClick={() => setStepIndex(result.steps.length - 1)}
          disabled={stepIndex === result.steps.length - 1}
        >
          Show Final Solution
        </Button>

        {/* Restart Button */}
        <Button 
          variant="contained" 
          color="primary" 
          fullWidth 
          sx={{ marginTop: 2 }} 
          onClick={() => navigate("/")}
        >
          Start Over
        </Button>
      </CardContent>
    </Card>
  );
}

export default SolvePage;
