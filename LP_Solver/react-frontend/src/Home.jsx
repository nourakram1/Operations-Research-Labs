import React, {useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { Button, TextField, Card, CardContent } from "@mui/material";
import { useLP } from "./LPContext"; // Import Context

function HomePage() {
  const navigate = useNavigate();
  const { numVariables, setNumVariables,
          numConstraints, setNumConstraints, 
          numGoals, setNumGoals,
          setObjective,
          setRestricted,
          setConstraintsMatrix,
          setConstraintsRelations,
          setGoalsMatrix,
          setGoalsRelations
  } = useLP();

  useEffect(() => {
    setNumVariables(2);
    setNumConstraints(1);
    setNumGoals(0);
  },[]);

  useEffect(() => {
          setObjective([Array(numVariables).fill(0)]);
          setRestricted(Array(numVariables).fill(true));
          setConstraintsMatrix(Array.from({ length: numConstraints }, () => Array(numVariables + 1).fill(0)));
          setConstraintsRelations(Array(numConstraints).fill("<="));
          setGoalsMatrix(Array.from({ length: numGoals }, () => Array(numVariables + 1).fill(0)));
          setGoalsRelations(Array(numGoals).fill("="));
      }, [numVariables, numConstraints, numGoals]);  

  const handleStart = () => {
    navigate("/input");
  };

  return (
    <Card sx={{ width: 1000, margin: "auto", padding: 2, textAlign: "center", borderRadius: 4, boxShadow: "0px 0px 20px rgba(0, 0, 0, 0.3)"  }}>
      <CardContent>
        <h2 className='title'>Linear Programming Solver</h2>
        <TextField label="Number of Variables" type="number" fullWidth margin="normal"
          value={numVariables} onChange={(e) => setNumVariables(Math.max(2, Number(e.target.value)))}/>
        <TextField label="Number of Constraints" type="number" fullWidth margin="normal"
          value={numConstraints} onChange={(e) => setNumConstraints(Math.max(1, Number(e.target.value)))}/>
        <TextField label="Number of Goals" type="number" fullWidth margin="normal"
          value={numGoals} onChange={(e) => setNumGoals(Math.max(0, Number(e.target.value)))}/>
        <Button variant="contained" color="primary" fullWidth sx={{ marginTop: 2 }} onClick={handleStart}>Start</Button>
      </CardContent>
    </Card>
  );
}

export default HomePage;
