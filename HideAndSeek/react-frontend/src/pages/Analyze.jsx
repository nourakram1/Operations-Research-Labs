import AnalyzeDashboard from '/src/components/AnalyzeDashboard/AnalyzeDashboard.jsx'
import {MathJaxContext} from "better-react-mathjax";
import {Container} from "@mui/material";

function Analyze() {
    return (
        <MathJaxContext>
            <Container sx={{marginTop: '50px', marginBottom: '50px'}}>
                <AnalyzeDashboard></AnalyzeDashboard>
            </Container>
        </MathJaxContext>
    )
}

export default Analyze
