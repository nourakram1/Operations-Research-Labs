import classes from './PlayGrid.module.css'
import { Typography } from "@mui/material";
import { useAppContext } from '/src/hooks/useAppContext.jsx'

import Ajv from "ajv"
import playSchema from '/src/../../schema/playSchema.json'
import playResponseSchema from '/src/../../schema/playResponseSchema.json'
import {useEffect, useRef} from "react";
import axios from "axios";

function PlayGrid() {
    const {
        n,
        m,
        PlayerRole,
        playerRole,
        gameBoard,
        hiderCoordinates, setHiderCoordinates,
        seekerCoordinates, setSeekerCoordinates,
        hiderProbabilities,
        seekerProbabilities,
        updateScore,
        updateRoundsWon
    } = useAppContext()

    const ajv = useRef(new Ajv({ allErrors: true }))
    const validatePlay = useRef(() => {})
    const validatePlayResponse = useRef(() => {})

    useEffect(() => {
        validatePlay.current = ajv.current.compile(playSchema)
        validatePlayResponse.current = ajv.current.compile(playResponseSchema)
    }, []);

    const hiderSelected = (row, col) => {
        return hiderCoordinates[0] === row && hiderCoordinates[1] === col
    }

    const seekerSelected = (row, col) => {
        return seekerCoordinates[0] === row && seekerCoordinates[1] === col
    }

    const handleCellOnClick = async (row, col) => {
        let hiderCoordinates, seekerCoordinates

        if (playerRole === PlayerRole.HIDER) {
            hiderCoordinates = [row, col]
        } else {
            seekerCoordinates = [row, col]
        }

        const request = {
            n,
            m,
        }

        if (playerRole === PlayerRole.HIDER) {
            request.probabilities = seekerProbabilities.current
        } else {
            request.probabilities = hiderProbabilities.current
        }

        const playRequestValid = validatePlay.current(request)
        console.log('Play request:', request)

        if (playRequestValid) {
            const response = await axios.post(`${import.meta.env.VITE_SERVER}/play`, request)

            const playResponseValid = validatePlayResponse.current(response.data)
            console.log('Play response:', response)

            if (playResponseValid) {
                const {row, col} = response.data
                if (playerRole === PlayerRole.HIDER) {
                    seekerCoordinates = [row, col]
                } else {
                    hiderCoordinates = [row, col]
                }

                setHiderCoordinates(hiderCoordinates)
                setSeekerCoordinates(seekerCoordinates)

                updateScore(hiderCoordinates, seekerCoordinates)
                updateRoundsWon(hiderCoordinates, seekerCoordinates)
            } else {
                console.log('Invalid play response:', validatePlayResponse.current.errors)
            }

        } else {
            console.log('Invalid play request:', validatePlay.current.errors)
        }
    }

    return (
        <div className={classes.gridContainer}>
            {gameBoard.current.map((row, rowIndex) => (
                <div key={rowIndex} className={classes.row}>
                    {row.map((item, colIndex) => (
                        <div key={colIndex}
                             className={`${classes.cell} ${classes[item.toLowerCase()]}
                                         ${hiderSelected(rowIndex, colIndex) ? classes['hiderSelected'] : ''}
                                         ${seekerSelected(rowIndex, colIndex) ? classes['seekerSelected'] : ''}`
                             }
                             onClick={async () => {await handleCellOnClick(rowIndex, colIndex)}}
                        >
                            <Typography fontSize={13} fontWeight={'bold'} variant='caption'>
                                <span>{item}</span>
                            </Typography>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    )
}

export default PlayGrid