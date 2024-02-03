import {useState} from 'react'
import Card from '../Card/Card.jsx'
import './HomePage.css'

function HomePage() {

    const [topic, setTopic] = useState("covid") // default covid
    const possibleTopics = ["covid", "flat-earth", "aliens"] 
    
    const changeTopic = (e) => {
        if (possibleTopics.includes(e.target.value)) {
            setTopic(e.target.value) // call data fetch here
        } else {
            setTopic("unavailable topic")
        }
    }

    return (
        <>
        <select id="topic_choices" onChange={(e) => changeTopic(e)}>
            <option className="option" value="covid">Covid-19</option>
            <option className="option" value="flat-earth">Flat Earth</option>
            <option className="option" value="aliens">Covid</option>
        </select>

        <p>Current chosen topic is: {topic}</p>
        <Card />
        <Card />
        <Card />
        <Card />
        <Card />
        </>
    );

    
}

export default HomePage