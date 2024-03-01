import {useState} from 'react'
import Video from '../Video/Video.jsx'
import InfoCard from '../InfoCard/InfoCard.jsx'
import './HomePage.css'

function HomePage() {

    const [topic, setTopic] = useState("covid") // default covid
    const possibleTopics = ["covid", "flat-earth", "alien-life"] 
    
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
        </>
    );

    
}

export default HomePage