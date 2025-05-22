import classes from './PlayDashboard.module.css'
import { Button, Paper, Typography } from "@mui/material";
import { useAppContext } from "/src/hooks/useAppContext.jsx";
import PlayGrid from "/src/components/PlayGrid/PlayGrid.jsx";
import { Link } from "react-router-dom";

function PlayDashboard() {
    const {
        PlayerRole,
        playerRole,
        hiderScore,
        seekerScore,
        hiderRoundsWon,
        seekerRoundsWon,
        hiderScoreChange,
        seekerScoreChange
    } = useAppContext()

    const formatScoreChange = (change) => {
        if (change === 0) return '';
        return change > 0 ? `(+${change})` : `(${change})`;
    }

    return (
        <Paper className={classes.paper} elevation={3} variant='outlined'>
            <Typography fontSize={25} fontWeight={'bold'}>
                You are the {playerRole === PlayerRole.HIDER ?
                <span className={classes.hider}>hider</span> :
                <span className={classes.seeker}>seeker</span>}!
            </Typography>

            <div className={classes.statsContainer}>
                <div className={classes.stats}>
                    <Typography
                        fontSize={15}
                        className={classes.hider}
                    >
                        Hider's score: {hiderScore} <span className={classes.scoreChange}>{formatScoreChange(hiderScoreChange)}</span>
                    </Typography>
                    <Typography
                        fontSize={15}
                        className={classes.hider}
                    >
                        Hider's rounds won: {hiderRoundsWon}
                    </Typography>
                </div>
                <div className={classes.stats}>
                    <Typography
                        fontSize={15}
                        className={classes.seeker}
                    >
                        Seeker's score: {seekerScore} <span className={classes.scoreChange}>{formatScoreChange(seekerScoreChange)}</span>
                    </Typography>
                    <Typography
                        fontSize={15}
                        className={classes.seeker}
                    >
                        Seeker's rounds won: {seekerRoundsWon}
                    </Typography>
                </div>
            </div>

            <div className={classes.prompt}>
                <Typography fontSize={14} fontWeight={'bold'} variant='caption' color='textSecondary'>
                    {`Please choose a place to ${playerRole === PlayerRole.HIDER ? 'hide' : 'seek'}`}
                </Typography>
            </div>

            <div className={classes.playGridContainer}>
                <PlayGrid />
            </div>

            <div className={classes.buttonContainer}>
                <Link to="/" className={classes.link}>
                    <Button variant="outlined" color="primary">
                        Back to setup
                    </Button>
                </Link>
                <Link to="/analyze" className={classes.link}>
                    <Button variant="contained" color="primary">
                        Analyze
                    </Button>
                </Link>
            </div>
        </Paper>
    )
}

export default PlayDashboard