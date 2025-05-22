import classes from './PlayDashboard.module.css'
import { Button, Paper, Typography, Box } from "@mui/material";
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
        seekerRoundsWon
    } = useAppContext()

    return (
        <Paper className={classes.paper} elevation={3}>
            <Typography variant="h4" fontWeight="bold" gutterBottom sx={{mb: 2.5}}>
                You are the {playerRole === PlayerRole.HIDER ?
                <span className={classes.hider}>hider</span> :
                <span className={classes.seeker}>seeker</span>}!
            </Typography>

            <Box className={classes.statsContainer}>
                <Box className={classes.stats}>
                    <Typography variant="h6" className={classes.hider} gutterBottom>
                        Hider Stats
                    </Typography>
                    <Typography variant="body1" className={classes.hider}>
                        Score: {hiderScore}
                    </Typography>
                    <Typography variant="body1" className={classes.hider}>
                        Rounds won: {hiderRoundsWon}
                    </Typography>
                </Box>
                <Box className={classes.stats}>
                    <Typography variant="h6" className={classes.seeker} gutterBottom>
                        Seeker Stats
                    </Typography>
                    <Typography variant="body1" className={classes.seeker}>
                        Score: {seekerScore}
                    </Typography>
                    <Typography variant="body1" className={classes.seeker}>
                        Rounds won: {seekerRoundsWon}
                    </Typography>
                </Box>
            </Box>

            <Box className={classes.prompt}>
                <Typography variant="subtitle1" color="textSecondary">
                    {`Please choose a place to ${playerRole === PlayerRole.HIDER ? 'hide' : 'seek'}`}
                </Typography>
            </Box>

            <Box className={classes.playGridContainer}>
                <PlayGrid />
            </Box>

            <Link to={'/analyze'} style={{ textDecoration: 'none' }}>
                <Button 
                    variant="contained" 
                    size="large"
                    sx={{
                        px: 3,
                        py: 1,
                        borderRadius: 2,
                        textTransform: 'none',
                        fontSize: '1.1rem'
                    }}
                >
                    Analyze Game
                </Button>
            </Link>
        </Paper>
    )
}

export default PlayDashboard