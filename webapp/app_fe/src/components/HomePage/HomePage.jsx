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
    const possibleSorts = ["verifiability", "upload_date"]

    useEffect(() => {
        getData()
        console.log('Effect Happened')
    }, [sortResultBy])

    function getData() {
        fetch("http://127.0.0.1:105/api/data?topic=" + topic + '&sort=' + sortResultBy, {method: 'GET'}) // can  sort by 'verifiability' or 'upload_date'
        .then(response => response.json())
        .then(data => setVideoData(data))
        .catch((error) => console.log('data fetching failed!, Here is the error: \n' + error));
        console.log('Get Data happened')
    }

    const changeTopic = (e) => {
        if (possibleTopics.includes(e.target.value)) {
            setTopic(e.target.value) // change topic which will trigger another data fetching and rerender.
        } else {
            setTopic("covid_philippines") // default
        }
    }

    const changeSort = (e) => {
        if (possibleSorts.includes(e.target.value)) {
            setSortResultBy(e.target.value) // change sort which will trigger another data fetching and rerender.
        } else {
            setSortResultBy('verifiability') // default
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
            <button onClick={() => getData()}>&#128269;</button>
        </div>
        <div className="sort">
            <select id="sort_choices" onChange={(e) => changeSort(e)}>
                <option className="option" value="verifiability">By Verifiability Score</option>
                <option className="option" value="upload_date">By Upload Date</option>
            </select>
        </div>
        <main> 
            <div>
                {videoData && videoData.map((video, index) => <Video onClick={() => setVideoShown(index)} toggled={index == videoShown} key={video.video_id} score={2} videoInfo={video}/>)}
            </div>
            {videoData && <InfoCard video={videoData[videoShown]} />}
        </main>
        </>
    );

    
}

export default HomePage