import AnalyzeDashboard from '/src/components/AnalyzeDashboard/AnalyzeDashboard.jsx'
import {MathJaxContext} from "better-react-mathjax";

function Analyze() {
    return (
        <MathJaxContext>
            <div className={'page-container'}>
                <AnalyzeDashboard></AnalyzeDashboard>
            </div>
        </MathJaxContext>
    )
}

export default Analyze
