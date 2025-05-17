import {useRef, useState} from "react";
import { AppContext } from '/src/context/AppContext.jsx'

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
        setHiderCoordinates([-1, -1])
        setSeekerCoordinates([-1, -1])
    }

    const calculateProximityFactor = (hiderCoordinates, seekerCoordinates) => {
        if (!proximity || equal(hiderCoordinates, seekerCoordinates))
            return 1

        return (Math.abs(hiderCoordinates[0] - seekerCoordinates[0]) +
            Math.abs(hiderCoordinates[1] - seekerCoordinates[1])) / (m + n)
    }

    const updateScore = (hiderCoordinates, seekerCoordinates) => {
        const flatHiderCoordinates = flatCoordinates(hiderCoordinates[0], hiderCoordinates[1])
        const flatSeekerCoordinates = flatCoordinates(seekerCoordinates[0], seekerCoordinates[1])

        let proximityFactor = calculateProximityFactor(hiderCoordinates, seekerCoordinates)

        setSeekerScore((prevSeekerScore) =>
            (prevSeekerScore - gameMatrix.current[flatHiderCoordinates][flatSeekerCoordinates]) * proximityFactor)
        setHiderScore((prevHiderScore) =>
            (prevHiderScore + gameMatrix.current[flatHiderCoordinates][flatSeekerCoordinates]) * proximityFactor)
    }

    const updateRoundsWon = (hiderCoordinates, seekerCoordinates) => {
        if (equal(hiderCoordinates, seekerCoordinates)) {
            setSeekerRoundsWon((prevSeekerRoundsWon) => prevSeekerRoundsWon + 1)
        } else {
            setHiderRoundsWon((prevHiderRoundsWon) => prevHiderRoundsWon + 1)
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
                hiderCoordinates, setHiderCoordinates,
                seekerCoordinates, setSeekerCoordinates,
                flatCoordinates,
                reset,
                equal,
                updateScore,
                updateRoundsWon
            }}>
            {children}
        </AppContext.Provider>
    )
}