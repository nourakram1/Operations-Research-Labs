import React from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";

function SimplexTableau({ data }) {
  return (
    <TableContainer component={Paper} sx={{ maxWidth: 1000, margin: "auto", mt: 3 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontWeight: "bold", textAlign: "center" }}>Basic</TableCell>
            {data.variables.map((varName, i) => (
              <TableCell
                key={i}
                sx={{
                  fontWeight: "bold",
                  textAlign: "center",
                  backgroundColor: i === data.enteringVariable ? "#ccffcc" : "inherit", // Highlight entering column
                }}
              >
                {varName}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.basicVariables.map((basicVar, rowIndex) => (
            <TableRow
              key={rowIndex}
              sx={rowIndex === data.leavingVariable ? { backgroundColor: "#ffcccc" } : {}}
            >
              <TableCell sx={{ fontWeight: "bold", textAlign: "center" }}>{basicVar}</TableCell>
              {data.tableau[rowIndex].map((value, colIndex) => (
                <TableCell
                  key={colIndex}
                  sx={{
                    textAlign: "center",
                    backgroundColor: colIndex === data.enteringVariable ? "#ccffcc" : "inherit",
                  }}
                >
                  {value}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default SimplexTableau;
