import {useState} from 'react'
import Card from '../Card/Card.jsx'
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
        <select id="topic_choices" onChange={(e) => changeTopic(e)}>
            <option className="option" value="covid">Covid-19</option>
            <option className="option" value="flat-earth">Flat Earth</option>
            <option className="option" value="alien-life">Alien Life</option>
        </select>

        <p>Current chosen topic is: {topic}</p>
        <Card score={1} />
        <Card score={2} />
        <Card score={3} />
        <Card score={4} />
        <Card score={5} />
        </>
    );

    
}

export default HomePage