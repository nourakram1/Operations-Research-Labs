import classes from './InputForm.module.css'
import React, { useEffect, useRef } from 'react'
import
{
    Box, Button, FormControlLabel,
    Paper, Switch, TextField,
    Typography,
} from '@mui/material'
import Ajv from 'ajv'
import axios from 'axios'
import ControlledRadioGroup from '/src/components/RadioGroup/ControlledRadioGroup.jsx'
import { useAppContext } from '/src/hooks/useAppContext.jsx'
import { useNavigate } from 'react-router-dom'

import generateGameSchema from '/src/../../schema/generate_request.json'
import generateGameResponseSchema from '/src/../../schema/generate_response.json'

function InputForm() {

    const {
        GameType,
        PlayerRole,
        gameType, setGameType,
        playerRole, setPlayerRole,
        proximity, setProximity,
        n, setN,
        m, setM,
        gameBoard,
        gameMatrix,
        hiderProbabilities,
        seekerProbabilities,
        reset,
        simulate
    } = useAppContext()

    const navigate = useNavigate()
    const ajv = useRef(new Ajv({ allErrors: true }))
    const validateGenerateGame = useRef(() => {})
    const validateGenerateGameResponse = useRef(() => {})

    useEffect(() => {
        validateGenerateGame.current = ajv.current.compile(generateGameSchema)
        validateGenerateGameResponse.current = ajv.current.compile(generateGameResponseSchema);
    }, [])

    const handleDimensionOnChange = (newDimension, setDimension) => {
        setDimension(Math.max(newDimension, 1))
    }

    const handleStartGame = async () => {
        let input = {
            n,
            m,
            proximity
        }

        const generateGameValid = validateGenerateGame.current(input)
        console.log('Generate game request:', input)

        if (generateGameValid) {
            const response = await axios.post(`${import.meta.env.VITE_SERVER}/generate`, input)
            const generateGameResponseValid = validateGenerateGameResponse.current(response.data)

            console.log('Generate game response:', response)
            if (generateGameResponseValid) {
                reset()

                gameBoard.current = response.data.gameBoard
                gameMatrix.current = response.data.gameMatrix
                hiderProbabilities.current = response.data.hiderProbabilities
                seekerProbabilities.current = response.data.hiderProbabilities

                if (gameType === GameType.SIMULATION) {
                    await simulate()
                    navigate('/analyze')
                }
                else {
                    navigate('/play')
                }
            }
            else {
                console.log('Invalid generate game response', validateGenerateGameResponse.current.errors)
            }
        }
        else {
            console.log('Invalid generate game request:', validateGenerateGame.current.errors)
        }
    }

    return (
        <Paper className={classes.paper} elevation={3} variant="outlined">
            <Typography fontSize={30} fontWeight={'bold'}>
                Hide and Seek Game Setup
            </Typography>

            <div className={classes.radioGroups}>
                <ControlledRadioGroup
                    id={'game-type-radio-group'}
                    label={'Game type'}
                    value={gameType}
                    onChange={(e) => setGameType(e.target.value)}
                    values={Object.values(GameType)}
                    labels={Object.values(GameType)}
                />
                {
                    gameType === GameType.INTERACTIVE && (
                        <ControlledRadioGroup
                            id={'player-role-radio-group'}
                            label={'Player role'}
                            value={playerRole}
                            onChange={(e) => setPlayerRole(e.target.value)}
                            values={Object.values(PlayerRole)}
                            labels={Object.values(PlayerRole)}
                        />
                    )
                }
            </div>

            <FormControlLabel
                control={<Switch checked={proximity}
                                 onChange={(e) => {setProximity(e.target.checked)}}
                />}
                label={'Proximity'}
            />

            <Box className={classes.dimensions}>
                <TextField
                    label={'N'}
                    type={'number'}
                    value={n}
                    onChange={(e) => handleDimensionOnChange(e.target.value, setN)}
                    required
                />
                <TextField
                    label={'M'}
                    type={'number'}
                    value={m}
                    onChange={(e) => handleDimensionOnChange(e.target.value, setM)}
                    required
                />
            </Box>

            <Button
                className={classes.startGame}
                variant="contained"
                fullWidth
                onClick={() => handleStartGame()}
            >
                Start game
            </Button>
        </Paper>
    )
}

export default InputForm
