import React, { createContext, useContext, useState } from "react";

const LPContext = createContext();

export const LPProvider = ({ children }) => {
  const [numVariables, setNumVariables] = useState(2);
  const [numConstraints, setNumConstraints] = useState(1);
  const [numGoals, setNumGoals] = useState(0);

  const [isMaximization, setIsMaximization] = useState(true);
  const [objectiveFunctionCoefficientsVector, setObjective] = useState([Array(numVariables).fill(0)]);
  const [restricted, setRestricted] = useState(Array(numVariables).fill(true));
  const [constraintsCoefficientsMatrix, setConstraintsMatrix] = useState(
    Array.from({ length: numConstraints }, () => Array(numVariables + 1).fill(0))
  );
  const [constraintsRelations, setConstraintsRelations] = useState(Array(numConstraints).fill("<="));
  const [goalsCoefficientsMatrix, setGoalsMatrix] = useState(
    Array.from({ length: numGoals }, () => Array(numVariables + 1).fill(0))
  );
  const [goalsRelations, setGoalsRelations] = useState(Array(numGoals).fill("="));
  const [method, setMethod] = useState("M");

  return (
    <LPContext.Provider value={{
      numVariables, setNumVariables, numConstraints, setNumConstraints, numGoals, setNumGoals,
      isMaximization, setIsMaximization,
      objectiveFunctionCoefficientsVector, setObjective,
      restricted, setRestricted,
      constraintsCoefficientsMatrix, setConstraintsMatrix,
      constraintsRelations, setConstraintsRelations,
      goalsCoefficientsMatrix, setGoalsMatrix,
      goalsRelations, setGoalsRelations,
      method, setMethod
    }}>
      {children}
    </LPContext.Provider>
  );
};

export const useLP = () => useContext(LPContext);
