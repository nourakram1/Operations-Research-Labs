import {useRef, useState} from "react";
import { AppContext } from '/src/context/AppContext.jsx'
import axios from "axios";

export default function AppProvider({children}) {
    const GameType = {
        INTERACTIVE: 'Interactive',
        SIMULATION: 'Simulation'
    }

    const PlayerRole = {
        HIDER: 'Hider',
        SEEKER: 'Seeker'
    }

    const CellDifficulty = {
        HARD: 'HARD',
        NEUTRAL: 'NEUTRAL',
        EASY: 'EASY'
    }

    const [gameType, setGameType] = useState(GameType.INTERACTIVE)
    const [playerRole, setPlayerRole] = useState(PlayerRole.HIDER)
    const [proximity, setProximity] = useState(false)
    const [n, setN] = useState(1)
    const [m, setM] = useState(1)

    const gameBoard = useRef(null)
    const gameMatrix = useRef(null)
    const hiderProbabilities = useRef(null)
    const seekerProbabilities = useRef(null)

    const [hiderScore, setHiderScore] = useState(1)
    const [seekerScore, setSeekerScore] = useState(1)
    const [hiderRoundsWon, setHiderRoundsWon] = useState(0)
    const [seekerRoundsWon, setSeekerRoundsWon] = useState(0)
    const [hiderScoreChange, setHiderScoreChange] = useState(0)
    const [seekerScoreChange, setSeekerScoreChange] = useState(0)

    const [hiderCoordinates, setHiderCoordinates] = useState([-1, -1])
    const [seekerCoordinates, setSeekerCoordinates] = useState([-1, -1])

    const equal = (arr1, arr2) => {
        if (arr1.length !== arr2.length)
            return false

        for (let i = 0; i < arr1.length; i++)
            if (arr1[i] !== arr2[i])
                return false

        return true
    }

    const flatCoordinates = (row, col) => {
        return row * m + col
    }

    const reset = () => {
        setHiderScore(0)
        setSeekerScore(0)
        setHiderRoundsWon(0)
        setSeekerRoundsWon(0)
        setHiderScoreChange(0)
        setSeekerScoreChange(0)
        setHiderCoordinates([-1, -1])
        setSeekerCoordinates([-1, -1])
    }

    const updateScore = (hiderCoordinates, seekerCoordinates) => {
        const flatHiderCoordinates = flatCoordinates(hiderCoordinates[0], hiderCoordinates[1])
        const flatSeekerCoordinates = flatCoordinates(seekerCoordinates[0], seekerCoordinates[1])
        const scoreChange = gameMatrix.current[flatHiderCoordinates][flatSeekerCoordinates]

        setSeekerScore((prevSeekerScore) => prevSeekerScore - scoreChange)
        setHiderScore((prevHiderScore) => prevHiderScore + scoreChange)
        setSeekerScoreChange(-scoreChange)
        setHiderScoreChange(scoreChange)
    }

    const updateRoundsWon = (hiderCoordinates, seekerCoordinates) => {
        if (equal(hiderCoordinates, seekerCoordinates)) {
            setSeekerRoundsWon((prevSeekerRoundsWon) => prevSeekerRoundsWon + 1)
        } else {
            setHiderRoundsWon((prevHiderRoundsWon) => prevHiderRoundsWon + 1)
        }
    }

    const simulate = async () => {
        const num = 100

        const hiderRequest = {
            n,
            m,
            probabilities: hiderProbabilities.current,
            num
        }

        const seekerRequest = {
            n,
            m,
            probabilities: seekerProbabilities.current,
            num
        }

        const hiderResponse = await axios.post(`${import.meta.env.VITE_SERVER}/simulate`, hiderRequest)
        const seekerResponse = await axios.post(`${import.meta.env.VITE_SERVER}/simulate`, seekerRequest)

        console.log('Hider response', hiderResponse)
        console.log('Seeker response', seekerResponse)

        const hiderMoves = hiderResponse.data.moves
        const seekerMoves = seekerResponse.data.moves

        for (let i = 0; i < num; i++) {
            const hiderCoordinates = [...hiderMoves[i]]
            const seekerCoordinates = [...seekerMoves[i]]
            updateScore(hiderCoordinates, seekerCoordinates)
            updateRoundsWon(hiderCoordinates, seekerCoordinates)
        }
    }

    return (
        <AppContext.Provider
            value={{
                GameType,
                PlayerRole,
                gameType, setGameType,
                playerRole, setPlayerRole,
                proximity, setProximity,
                n, setN,
                m, setM,
                CellDifficulty,
                gameBoard,
                gameMatrix,
                hiderProbabilities,
                seekerProbabilities,
                hiderScore, setHiderScore,
                seekerScore, setSeekerScore,
                hiderRoundsWon, setHiderRoundsWon,
                seekerRoundsWon, setSeekerRoundsWon,
                hiderScoreChange, setHiderScoreChange,
                seekerScoreChange, setSeekerScoreChange,
                hiderCoordinates, setHiderCoordinates,
                seekerCoordinates, setSeekerCoordinates,
                flatCoordinates,
                reset,
                equal,
                updateScore,
                updateRoundsWon,
                simulate
            }}>
            {children}
        </AppContext.Provider>
    )
}