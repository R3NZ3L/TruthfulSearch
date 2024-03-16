import './HomePage.css';
import Video from '../Video/Video.jsx';
import InfoCard from '../InfoCard/InfoCard.jsx';
import { useState, useEffect } from 'react';

function HomePage() {

    const [topic, setTopic] = useState("covid_philippines") // default covid
    const possibleTopics = ["covid_philippines", "covid_vaccine", "israel-palestine_conflict_history"] 
    const [videoData, setVideoData] = useState(null)
    const [videoShown, setVideoShown] = useState(0)
    const [sortResultBy, setSortResultBy] = useState('verifiability')

    useEffect(() => {
        getData()
    }, [topic, sortResultBy]);

    function getData() {
       fetch("http://127.0.0.1:105/api/data?topic=" + topic + '&sort=' + sortResultBy, {method: 'GET'}) // can  sort by 'verifiability' or 'upload_date'
       .then(response => response.json()).then(data => setVideoData(data))
    }

    const changeTopic = (e) => {
        if (possibleTopics.includes(e.target.value)) {
            setTopic(e.target.value) // change topic which will trigger another data fetching and rerender.
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
                {videoData && videoData.map((video, index) => <Video onClick={() => setVideoShown(index)} key={video.video_id} score={2} videoInfo={video}/>)}
            </div>
            {videoData && <InfoCard video={videoData[videoShown]} />}
        </main>
        </>
    );

    
}

export default HomePage