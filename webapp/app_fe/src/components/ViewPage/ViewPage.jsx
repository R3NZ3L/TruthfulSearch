import { useLocation } from "react-router-dom";

function ViewPage(){

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const value = queryParams.get('id')

    return (
        <iframe width="620" height="415"
            src={`https://www.youtube.com/embed/${value}`}>
        </iframe>
    )
}

export default ViewPage