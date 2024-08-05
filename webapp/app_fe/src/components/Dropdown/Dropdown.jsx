import './Dropdown.css'
import { useState } from "react"

function Dropdown({ sortResultBy, setSortResultBy }) {
    const possibleSorts = ["channel_verifiability", "video_rank", "upload_date"]
    const [menuShow, setMenuShow] = useState(false)

    const sortValue = (possibleSort) => { 
        return  possibleSort == "channel_verifiability" ? "By Channel Verifiability Score" :
                possibleSort == "video_rank" ? "By Computed Video Rank" : 
                possibleSort == "upload_date" ? "By Upload Date" :"Error"
    }

    const isActive = (sortResultBy, possibleSort) => {
        return  sortResultBy == possibleSort ? true :
                sortResultBy == possibleSort ? true : false
    }

    return (
        <div className="dropdown">
            <div className={`select ${menuShow && 'select-clicked'}`} onClick={() => setMenuShow(!menuShow)}>
                <span className="selected">
                    {sortValue(sortResultBy)}
                </span>
                <div className={`caret ${menuShow && 'caret-rotate'}`}></div>
            </div>

            <ul className={`menu ${menuShow && 'menu-open'}`}>
                {possibleSorts.map(possibleSort => (
                    <li className={`${isActive(sortResultBy, possibleSort) && 'active'}`} key={possibleSort} value={possibleSort} onClick={e => {setSortResultBy(possibleSort); setMenuShow(!menuShow);}}>
                        {sortValue(possibleSort)}
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default Dropdown