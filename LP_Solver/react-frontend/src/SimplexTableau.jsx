import React from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";
import { InlineMath } from "react-katex";
import "katex/dist/katex.min.css";

function SimplexTableau({ data }) {
  return (
    <TableContainer component={Paper} sx={{ maxWidth: 1000, mt: 3, mb: 3, boxShadow: "none", border: "solid grey 2px" }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontWeight: "bold", textAlign: "center" }}><InlineMath>{'\\text{Basic}'}</InlineMath></TableCell>
            {data.variables.map((varName, i) => (
              <TableCell
                key={i}
                sx={{
                  fontWeight: "bold",
                  textAlign: "center",
                  backgroundColor: i === data.enteringVariable ? "#ccffcc" : "inherit", // Highlight entering column
                }}
              >
              <InlineMath>{varName}</InlineMath>
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
              <TableCell sx={{ fontWeight: "bold", textAlign: "center" }}><InlineMath>{basicVar}</InlineMath></TableCell>
              {data.tableau[rowIndex].map((value, colIndex) => (
                <TableCell
                  key={colIndex}
                  sx={{
                    textAlign: "center",
                    backgroundColor: colIndex === data.enteringVariable ? "#ccffcc" : "inherit",
                  }}
                >
                  <InlineMath>{value}</InlineMath>
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
