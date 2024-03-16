import './HomePage.css';
import Video from '../Video/Video.jsx';
import InfoCard from '../InfoCard/InfoCard.jsx';
import { useState, useEffect } from 'react';

function HomePage() {

    const [topic, setTopic] = useState("covid") // default covid
    const possibleTopics = ["covid", "flat-earth", "alien-life"] 
    const [videoData, setVideoData] = useState([])
    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async ()=> {
        try{
            const response = await fetch("http://127.0.0.1:105/api/data", {method: 'GET'})
            const message =  await response.json()
            setVideoData(message)
        } catch(error) {
            console.log("Error", error)
        }
    }

    const changeTopic = (e) => {
        if (possibleTopics.includes(e.target.value)) {
            setTopic(e.target.value) // call data fetch here
        } else {
            setTopic("unavailable topic")
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
                {videoData.map(video =><Video key={video.id} score={2} videoInfo={video}/>)}
            </div>
            <InfoCard />
        </main>
        </>
    );

    
}

export default HomePage