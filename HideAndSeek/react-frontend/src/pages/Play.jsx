import PlayDashboard from "/src/components/PlayDashboard/PlayDashboard.jsx";
import {Container} from "@mui/material";

function Play() {
    return (
        <Container sx={{marginTop: '50px', marginBottom: '50px'}}>
            <PlayDashboard />
        </Container>
    )
}

export default Play