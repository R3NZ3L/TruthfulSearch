import './HomePage.css';
import Video from '../Video/Video.jsx';
import InfoCard from '../InfoCard/InfoCard.jsx';
import { useState, useEffect } from 'react';

function HomePage() {

    const [topic, setTopic] = useState("covid_philippines") // default covid
    const possibleTopics = ["covid_philippines", "covid_vaccine", "israel-palestine_conflict_history"] 
    const [videoData, setVideoData] = useState(null)
    console.log("I rendered")

    useEffect(() => {
        getData()
    }, [topic]);

    function getData() {
       fetch("http://127.0.0.1:105/api/data?topic=" + topic, {method: 'GET'})
       .then(response => response.json()).then(data => setVideoData(data)).finally(console.log('I got data'))
    }

    const changeTopic = (e) => {
        if (possibleTopics.includes(e.target.value)) {
            setTopic(e.target.value) // call data fetch here
        } else {
            setTopic('covid_philippines') // default
        }
    }

    return (
        <>
        <span id="brand">VERIFYVID</span>
        <div id="search_bar">
            <select id="topic_choices" onChange={(e) => changeTopic(e)}>
                <option className="option" value="covid_philippines">Covid Philippines</option>
                <option className="option" value="covid_vaccine">Covid Vaccine</option>
                <option className="option" value="israel-palestine_conflict_history">Israel Palestine Conflict History</option>
            </select>
            <button>&#128269;</button>
        </div>
        <main> 
            <div>
                {&&}
                {console.log(JSON.stringify(videoData[1]))}  
                {JSON.stringify(videoData[1])}
                {videoData.map(video => <Video key={video.video_id} score={2} videoInfo={video}/>)}
            </div>
            <InfoCard/>
        </main>
        </>
    );

    
}

export default HomePage