import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button, Card, CardContent, Paper, Typography } from "@mui/material";
import SimplexTableau from "./SimplexTableau"; // Import the table component
import { InlineMath } from "react-katex";
import { MathJax, MathJaxContext } from "better-react-mathjax";
import "katex/dist/katex.min.css";

const config = {
  loader: { load: ["[tex]/html"] },
  tex: {
    packages: { "[+]": ["html"] },
    inlineMath: [
      ["$", "$"],
      ["\\(", "\\)"]
    ],
    displayMath: [
      ["$$", "$$"],
      ["\\[", "\\]"]
    ]
  }
};

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
    variables: step.variables.concat('\\text{Soltuion}'), // Header row
    basicVariables: step.zRowsSymbols.concat(step.basicVariables), // First column (basic variables)
    tableau: step.simplexMatrix, // Matrix with first column
    enteringVariable: step.enteringVariableIndex, // Column index for highlighting
    leavingVariable: step.leavingVariableIndex != null ? step.leavingVariableIndex + step.zRowsSymbols.length : null
  }
  return (
    <MathJaxContext version={3} config={config}>
      <Card sx={{ width: 1000, margin: "auto", padding: 3 }}>
      <CardContent>
        <h2 className='title'>Solution</h2>

        {/* Comment Section */}
        <Typography
          variant="subtitle1"
          sx={{ backgroundColor: "#f0f0f0", padding: 2, borderRadius: 2, mb: 2 }}
        >
          <MathJax>{`Step ${stepIndex + 1}: ` + step.comment}</MathJax>
        </Typography>

        {/* Simplex Tableau Component */}
        <Paper sx={{boxShadow: "none"}}>
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
    </MathJaxContext>
  );
}

export default SolvePage;
