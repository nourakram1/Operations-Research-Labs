import React, { useState, useMemo } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { Button, TextField, Card, CardContent, Select, MenuItem, FormControlLabel, Checkbox, FormControl, InputLabel, Radio, RadioGroup } from "@mui/material";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";

function InputPage() {
  const [isMaximization, setIsMaximization] = useState(true);
  const { numVariables, numConstraints, numGoals } = useParams();
  const navigate = useNavigate();
  const variables = Number(numVariables);
  const constraintsNum = Number(numConstraints);
  const goalsNum = Number(numGoals);

  const [objectiveFunctionCoefficientsVector, setObjective] = useState(Array(variables).fill(0));
  const [restricted, setRestricted] = useState(Array(variables).fill(true));
  const [constraintsCoefficientsMatrix, setConstraintsMatrix] = useState(
    Array.from({ length: constraintsNum }, () => Array(variables + 1).fill(0))
  );
  const [constraintsRelations, setConstraintsRelations] = useState(Array(constraintsNum).fill("<="));
  const [goalsCoefficientsMatrix, setGoalsMatrix] = useState(
    Array.from({ length: goalsNum }, () => Array(variables + 1).fill(0))
  );
  const [goalsRelations, setGoalsRelations] = useState(Array(goalsNum).fill("="));
  const [method, setMethod] = useState("Default");

  const hasGEQorEQ = useMemo(() => {
    if(constraintsRelations.some((rel) => rel === "<=")){
      setMethod("Default")
    }else{
      setMethod("M")
    }
    return constraintsRelations.some((rel) => rel !== "<=");
  }, [constraintsRelations, goalsRelations]);

  const handleSolve = async () => {
    const requestData = {
      method,
      constraintsCoefficientsMatrix,
      constraintsRelations,
      goalsCoefficientsMatrix,
      goalsRelations,
      objectiveFunctionCoefficientsVector,
      restricted,
    };

    console.log("Request Data:", requestData);
    try {
      const response = await axios.post("http://your-backend-url/solve", requestData);
      console.log("Response:", response.data);
      navigate("/solve", { state: { result: response.data } });
    } catch (error) {
      console.error("Error sending request:", error);
    }
  };


  const handleDragEnd = (result) => {
    if (!result.destination) return;
    const newGoalsMatrix = structuredClone(goalsCoefficientsMatrix);
    const newGoalsRelations = structuredClone(goalsRelations);
    
    const [reorderedGoal] = newGoalsMatrix.splice(result.source.index, 1);
    const [reorderedRelation] = newGoalsRelations.splice(result.source.index, 1);
    
    newGoalsMatrix.splice(result.destination.index, 0, reorderedGoal);
    newGoalsRelations.splice(result.destination.index, 0, reorderedRelation);
    
    setGoalsMatrix(newGoalsMatrix);
    setGoalsRelations(newGoalsRelations);
  };

  const handleNumberChange = (value) => {
    // Allow "-" and "." while typing
    if (value === "-" || value === "." || value.endsWith(".")) return value;
    if (value === "0-") return "-";
  
    // Handle cases like "0-5" correctly
    if (/^0-\d+/.test(value)) return Number("-" + value.slice(2)); // Convert "0-5" to -5
  
    // Ensure only valid numbers (including negatives & decimals)
    if (!/^-?\d*\.?\d*$/.test(value)) return null;
  
    // Remove leading zeros for positive numbers (e.g., "007" → "7") but allow "0." for decimals
    if (!value.startsWith("0.") && !value.startsWith("-0.")) {
      value = value.replace(/^(?!-0)-?0+(?=\d)/, "");
    }
  
    // If it ends with ".", return as is (for user experience while typing)
    if (value.endsWith(".") || value.includes(".")&& value.endsWith("0")) return value;
  
    // Convert to number if it's a valid numeric input
    return value === "" || value === "-" ? 0 : parseFloat(value);
  };
  
  

  return (
    <Card sx={{ width: 1000, margin: "auto", padding: 2 }}>
      <CardContent>
      {goalsNum === 0 ? (
          <>
            <h2>Enter Objective Function</h2>
            <RadioGroup
              row
              value={isMaximization ? "max" : "min"}
              onChange={(e) => setIsMaximization(e.target.value === "max")}
            >
              <FormControlLabel value="max" control={<Radio />} label="Maximization" />
              <FormControlLabel value="min" control={<Radio />} label="Minimization" />
            </RadioGroup>
        <div style={{ display: "flex", gap: "10px", alignItems: "center", flexWrap: "nowrap" }}>
          {objectiveFunctionCoefficientsVector.map((coef, index) => (
            <div key={index} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
              <TextField label={`x${index + 1}`} type="text" variant="outlined" value={coef} 
                onChange={(e) => {
                  let inputValue = handleNumberChange(e.target.value);
                  const newObj = [...objectiveFunctionCoefficientsVector];
                  newObj[index] = inputValue === "" ? "0" : inputValue;
                  setObjective(newObj);
                }}
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={!restricted[index]}
                    onChange={(e) => {
                      const newRestricted = [...restricted];
                      newRestricted[index] = !e.target.checked;
                      setRestricted(newRestricted);
                    }}
                  />
                }
                label="URS"
              />
            </div>
          ))}
        </div>
          </>
        ) :(<>
          <h2>Select Unrestricted Variables</h2>
          <div style={{ display: "flex", gap: "10px", flexWrap: "nowrap" }}>
            {Array.from({ length: variables }, (_, index) => (
              <FormControlLabel
                key={index}
                control={
                  <Checkbox
                    checked={!restricted[index]}
                    onChange={(e) => {
                      const newRestricted = [...restricted];
                      newRestricted[index] = !e.target.checked;
                      setRestricted(newRestricted);
                    }}
                  />
                }
                label={`x${index + 1}`}
              />
            ))}
          </div></>)}

        <h2>Enter Constraints</h2>
        {constraintsCoefficientsMatrix.map((row, rowIndex) => (
          <div key={rowIndex} style={{ display: "flex", gap: "10px", marginBottom: "10px", alignItems: "center" }}>
            {row.slice(0, -1).map((value, colIndex) => (
              <TextField
                key={colIndex}
                type="text"
                variant="outlined"
                value={value}
                onChange={(e) => {
                  let inputValue = handleNumberChange(e.target.value);
                  const newConstraints = [...constraintsCoefficientsMatrix];
                  newConstraints[rowIndex][colIndex] = inputValue === "" ? "0" : inputValue;
                  setConstraintsMatrix(newConstraints);
                }}
                label={`x${colIndex + 1}`}
              />
            ))}
            <Select
              value={constraintsRelations[rowIndex]}
              onChange={(e) => {
                const newRelations = [...constraintsRelations];
                newRelations[rowIndex] = e.target.value;
                setConstraintsRelations(newRelations);
              }}
            >
              <MenuItem value="<=">≤</MenuItem>
              <MenuItem value=">=">≥</MenuItem>
              <MenuItem value="=">=</MenuItem>
            </Select>
            <TextField
              type="text"
              variant="outlined"
              value={row[variables]}
              onChange={(e) => {
                let inputValue = handleNumberChange(e.target.value);
                const newConstraints = [...constraintsCoefficientsMatrix];
                newConstraints[rowIndex][variables] = inputValue === "" ? "0" : inputValue;
                setConstraintsMatrix(newConstraints);
              }}
              label="RHS"
            />
          </div>
        ))}

        {numGoals > 0 && <h2>Enter Goals</h2>}
        <DragDropContext onDragEnd={handleDragEnd}>
          <Droppable droppableId="goals">
            {(provided) => (
              <div {...provided.droppableProps} ref={provided.innerRef}>
                {goalsCoefficientsMatrix.map((row, rowIndex) => (
                  <Draggable key={`goal-${rowIndex}`} draggableId={`goal-${rowIndex}`} index={rowIndex}>
                    {(provided, snapshot) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        style={{
                          ...provided.draggableProps.style,
                          background: snapshot.isDragging ? "#ddd" : "lightgray",
                          padding: "10px",
                          borderRadius: "5px",
                          marginBottom: "10px",
                          display: "flex",
                          gap: "10px",
                          alignItems: "center",
                        }}
                      >
                        {row.slice(0, -1).map((value, colIndex) => (
                          <TextField
                            key={colIndex}
                            type="text"
                            variant="outlined"
                            value={value}
                            onChange={(e) => {
                              let inputValue = handleNumberChange(e.target.value);
                              const newGoals = [...goalsCoefficientsMatrix];
                              newGoals[rowIndex][colIndex] = inputValue === "" ? "0" : inputValue;
                              setGoalsMatrix(newGoals);
                            }}
                            label={`x${colIndex + 1}`}
                          />
                        ))}
                        <Select
                          value={goalsRelations[rowIndex]}
                          onChange={(e) => {
                            const newRelations = [...goalsRelations];
                            newRelations[rowIndex] = e.target.value;
                            setGoalsRelations(newRelations);
                          }}
                        >
                          <MenuItem value="<=">≤</MenuItem>
                          <MenuItem value=">=">≥</MenuItem>
                          <MenuItem value="=">=</MenuItem>
                        </Select>
                        <TextField type="text" variant="outlined" value={row[variables]} 
                          onChange={(e) => {
                              let inputValue = handleNumberChange(e.target.value);
                              const newGoals = [...goalsCoefficientsMatrix];
                              newGoals[rowIndex][variables] = inputValue === "" ? "0" : inputValue;
                              setGoalsMatrix(newGoals);
                          }} label="RHS" 
                        />
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>

        {hasGEQorEQ && (
          <FormControl fullWidth sx={{ marginTop: 2 }}>
            <InputLabel>Choose Method</InputLabel>
            <Select value={method} onChange={(e) => setMethod(e.target.value)}>
              <MenuItem value="M">M Method</MenuItem>
              <MenuItem value="TP">Two-Phase</MenuItem>
            </Select>
          </FormControl>
        )}

        <Button variant="contained" color="primary" fullWidth sx={{ marginTop: 2 }} onClick={handleSolve}>
          Solve
        </Button>
      </CardContent>
    </Card>
  );
}

export default InputPage;
