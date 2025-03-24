import React from "react";
import {Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow} from "@mui/material";
import {InlineMath} from "react-katex";
import "katex/dist/katex.min.css";

function SimplexTableau({ data }) {
  return (
    <TableContainer component={Paper} sx={{ maxWidth: 1000, mt: 3, mb: 3, boxShadow: "none", border: "solid grey 3px",  borderRadius: 2 }}>
      <Table>
        <TableHead sx={{ borderBottom: "3px solid grey" }}> {/* Line after header */}
          <TableRow>
            <TableCell
              sx={{ fontWeight: "bold", textAlign: "center", borderRight: "3px solid grey" }} // Line after first column
            >
              <InlineMath>{'\\text{Basic}'}</InlineMath>
            </TableCell>
            {data.variables.map((varName, i) => (
              <TableCell
                key={i}
                sx={{
                  fontWeight: "bold",
                  textAlign: "center",
                  backgroundColor: i === data.enteringVariable ? "#ccffcc" : "inherit",
                  borderRight: i === data.variables.length - 2 ? "3px solid grey" : "inherit", // Line before last column
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
              sx={{
                backgroundColor: rowIndex === data.leavingVariable ? "#ffcccc" : "inherit",
                borderBottom: rowIndex === data.breakIndex - 1 ? "3px solid rgb(194, 194, 194)" : "inherit", // Line before breakIndex
              }}
            >
              <TableCell
                sx={{ fontWeight: "bold", textAlign: "center", borderRight: "3px solid grey" }} // Line after first column
              >
                <InlineMath>{basicVar}</InlineMath>
              </TableCell>
              {data.tableau[rowIndex].map((value, colIndex) => (
                <TableCell
                  key={colIndex}
                  sx={{
                    textAlign: "center",
                    backgroundColor: colIndex === data.enteringVariable ? "#ccffcc" : "inherit",
                    borderRight: colIndex === data.tableau[rowIndex].length - 2 ? "3px solid grey" : "inherit", // Line before last column
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
