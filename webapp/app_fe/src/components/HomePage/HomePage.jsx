import './HomePage.css';
import Video from '../Video/Video.jsx';
import InfoCard from '../InfoCard/InfoCard.jsx';
import { useState, useEffect } from 'react';

function HomePage() {

    const [topic, setTopic] = useState("covid") // default covid
    const possibleTopics = ["covid", "flat-earth", "alien-life"] 
    const [data, setData] = useState({})
    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async ()=> {
        try{
        const response = await fetch("http://127.0.0.1:105/api/data", {method: 'GET'})
        const message =  await response.json()
        console.log(response)
        //setData(message)
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

    /* Possible scores for now
        1 = 0-19%
        2 = 20-39%
        3 = 40-59%        
        4 = 60-79%
        5 = 80-100%
    */

    return (
        <>
        <span id="brand">VERIFYVID</span>
        <div id="search_bar">
            <select id="topic_choices" onChange={(e) => changeTopic(e)}>
                <option className="option" value="covid">Covid-19</option>
                <option className="option" value="flat-earth">Flat Earth</option>
                <option className="option" value="alien-life">Alien Life</option>
            </select>
            <button>&#128269;</button>
        </div>
        <main> 
            <div>
                <Video score={1} />
                <Video score={2} />
                <Video score={3} />
                <Video score={4} />
                <Video score={5} />
            </div>
            <InfoCard />
        </main>
        Server returned this value: {data}
        </>
    );

    
}

export default HomePage