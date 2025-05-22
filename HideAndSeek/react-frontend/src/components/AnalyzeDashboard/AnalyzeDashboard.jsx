import classes from './AnalyzeDashboard.module.css'
import { Paper, Table, TableBody, TableCell, TableContainer, TableRow, Typography} from "@mui/material";
import { useAppContext } from "/src/hooks/useAppContext.jsx";
import {MathJax} from "better-react-mathjax";

function PlayDashboard() {
    const {
        n,
        m,
        hiderScore,
        seekerScore,
        hiderRoundsWon,
        seekerRoundsWon,
        gameMatrix,
        flatCoordinates,
        hiderProbabilities,
        seekerProbabilities,
        gameBoard,
    } = useAppContext()


    const tabulateGameMatrix = () => {
        let table = structuredClone(gameMatrix.current)
        const header = ['']

        for (let i = 0; i < n; i++) {
            for (let j = 0; j < m; j++) {
                header.push(`S_{${i + 1}${j + 1}}`)
                table[flatCoordinates(i, j)].unshift(`H_{${i + 1}${j + 1}}`)
            }
        }
        table.unshift(header)

        const latexTable = table.map((row) =>
            row.map((element) =>
                `$$${element}$$`
            )
        )

        console.log(latexTable);
        return latexTable
    }

    const tabulateProbabilities = (probabilities, symbol) => {
        let table = structuredClone(probabilities)

        for (let i = 0; i < n; i++) {
            for (let j = 0; j < m; j++) {
                table[flatCoordinates(i, j)] = [`$$${symbol}_{${i + 1}${j + 1}}$$`,
                    `$$${table[flatCoordinates(i, j)]}$$`]
            }
        }

        return table
    }

    return (
        <Paper className={classes.paper}>
            <div className={classes.statsContainer}>
                <Typography fontSize={30} fontWeight={'bold'}>
                    Statistics
                </Typography>
                <div className={classes.stats}>
                    <div className={classes.score}>
                        <Typography fontSize={20}>
                            Hider's score: {hiderScore}
                        </Typography>
                        <Typography fontSize={20}>
                            Hider's rounds won: {hiderRoundsWon}
                        </Typography>
                    </div>
                    <div className={classes.score}>
                        <Typography fontSize={20}>
                            Seeker's score: {seekerScore}
                        </Typography>
                        <Typography fontSize={20}>
                            Seeker's rounds won: {seekerRoundsWon}
                        </Typography>
                    </div>
                </div>
            </div>

            <div className={classes.gameBoard}>
                <Typography fontSize={30} fontWeight={'bold'}>
                    Game board
                </Typography>
                <TableContainer className={classes.gameBoardTable}>
                    <Table>
                        <TableBody>
                            {
                                gameBoard.current.map((row, rowIndex) =>
                                    <TableRow key={rowIndex}>
                                        {
                                            row.map((cell, colIndex) =>
                                                <TableCell
                                                    key={colIndex}
                                                    align={'center'}
                                                    className={`${classes[cell.toLowerCase()]} ${classes.cell}`}
                                                >
                                                    <Typography fontSize={15} fontWeight={'bold'} variant={'caption'}>
                                                        {cell}
                                                    </Typography>
                                                </TableCell>
                                            )
                                        }
                                    </TableRow>
                                )
                            }
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>

            <div className={classes.gameMatrix}>
                <Typography fontSize={30} fontWeight={'bold'}>
                    Game matrix
                </Typography>
                <Table className={classes.tableContainer}>
                    <TableBody>
                        {
                            tabulateGameMatrix().map((row, rowIndex) =>
                                <TableRow key={rowIndex}>
                                    {
                                        row.map((cell, colIndex) =>
                                            <TableCell key={colIndex}>
                                                <MathJax>
                                                    {cell}
                                                </MathJax>
                                            </TableCell>
                                        )
                                    }
                                </TableRow>
                            )
                        }
                    </TableBody>
                </Table>
            </div>

            <div className={classes.probabilities}>
                <Typography fontSize={30} fontWeight={'bold'}>
                    Probabilities
                </Typography>
                <div className={classes.probabilityTables}>
                    <Table className={classes.tableContainer}>
                        <TableBody>
                            {
                                tabulateProbabilities(hiderProbabilities.current, 'H').map((row, rowIndex) => (
                                    <TableRow key={rowIndex}>
                                        {
                                            row.map((cell, colIndex) => (
                                                <TableCell key={colIndex}>
                                                    <MathJax>
                                                        {cell}
                                                    </MathJax>
                                                </TableCell>
                                            ))
                                        }
                                    </TableRow>
                                ))
                            }
                        </TableBody>
                    </Table>
                    <Table className={classes.tableContainer}>
                        <TableBody>
                            {
                                tabulateProbabilities(seekerProbabilities.current, 'S').map((row, rowIndex) => (
                                    <TableRow key={rowIndex}>
                                        {
                                            row.map((cell, colIndex) => (
                                                <TableCell key={colIndex}>
                                                    <MathJax>
                                                        {cell}
                                                    </MathJax>
                                                </TableCell>
                                            ))
                                        }
                                    </TableRow>
                                ))
                            }
                        </TableBody>
                    </Table>
                </div>
            </div>
        </Paper>
    )
}

export default PlayDashboard