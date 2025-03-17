import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Button, TextField, Card, CardContent, Select, MenuItem, FormControl, InputLabel } from "@mui/material";

function InputPage() {
  const { numVariables, numConstraints, numGoals } = useParams();
  const navigate = useNavigate();
  const variables = Number(numVariables);
  const constraintsNum = Number(numConstraints);
  const goalsNum = Number(numGoals);

  const [objective, setObjective] = useState(Array(variables).fill(0));
  const [constraints, setConstraints] = useState(
    Array(constraintsNum).fill({ coefficients: Array(variables).fill(0), sign: "<=", rhs: 0 })
  );
  const [goals, setGoals] = useState(
    Array(goalsNum).fill({ coefficients: Array(variables).fill(0), rhs: 0 })
  );
  const [method, setMethod] = useState("M");

  const hasGEQorEQ = constraints.some(({ sign }) => sign === ">=" || sign === "=");

  return (
    <Card sx={{ maxWidth: 700, margin: "auto", padding: 2 }}>
      <CardContent>
        <h2>Step 2: Enter Objective Function</h2>
        <div style={{ display: "flex", gap: "10px" }}>
          {objective.map((coef, index) => (
            <TextField key={index} label={`x${index + 1}`} type="number" variant="outlined" value={coef} 
              onChange={(e) => {
                const newObj = [...objective];
                newObj[index] = Number(e.target.value);
                setObjective(newObj);
              }}
            />
          ))}
        </div>

        <h3>Constraints</h3>
        {constraints.map(({ coefficients, sign, rhs }, rowIndex) => (
          <div key={rowIndex} style={{ display: "flex", gap: "10px", marginBottom: "10px", alignItems: "center" }}>
            {coefficients.map((value, colIndex) => (
              <TextField key={colIndex} type="number" variant="outlined" value={value} 
                onChange={(e) => {
                  const newConstraints = [...constraints];
                  newConstraints[rowIndex].coefficients[colIndex] = Number(e.target.value);
                  setConstraints(newConstraints);
                }} label={`x${colIndex + 1}`} 
              />
            ))}
            <Select value={sign} onChange={(e) => {
              const newConstraints = [...constraints];
              newConstraints[rowIndex].sign = e.target.value;
              setConstraints(newConstraints);
            }}>
              <MenuItem value="<=">≤</MenuItem>
              <MenuItem value=">=">≥</MenuItem>
              <MenuItem value="=">=</MenuItem>
            </Select>
            <TextField type="number" variant="outlined" value={rhs} 
              onChange={(e) => {
                const newConstraints = [...constraints];
                newConstraints[rowIndex].rhs = Number(e.target.value);
                setConstraints(newConstraints);
              }} label="RHS" 
            />
          </div>
        ))}

        {numGoals > 0 && <h3>Goals</h3>}
        {goals.map(({ coefficients, rhs }, rowIndex) => (
          <div key={rowIndex} style={{ display: "flex", gap: "10px", marginBottom: "10px", alignItems: "center" }}>
            {coefficients.map((value, colIndex) => (
              <TextField key={colIndex} type="number" variant="outlined" value={value} 
                onChange={(e) => {
                  const newGoals = [...goals];
                  newGoals[rowIndex].coefficients[colIndex] = Number(e.target.value);
                  setGoals(newGoals);
                }} label={`x${colIndex + 1}`} 
              />
            ))}
            <span style={{ fontSize: "1.5rem" }}>=</span>
            <TextField type="number" variant="outlined" value={rhs} 
              onChange={(e) => {
                const newGoals = [...goals];
                newGoals[rowIndex].rhs = Number(e.target.value);
                setGoals(newGoals);
              }} label="RHS" 
            />
          </div>
        ))}

        {hasGEQorEQ && (
          <FormControl fullWidth sx={{ marginTop: 2 }}>
            <InputLabel>Choose Method</InputLabel>
            <Select value={method} onChange={(e) => setMethod(e.target.value)}>
              <MenuItem value="M">M Method</MenuItem>
              <MenuItem value="Two-Phase">Two-Phase</MenuItem>
            </Select>
          </FormControl>
        )}

        <Button variant="contained" color="primary" fullWidth sx={{ marginTop: 2 }} onClick={() => navigate("/solve")}>
          Solve
        </Button>
      </CardContent>
    </Card>
  );
}

export default InputPage;
