import random_thumbnail from '../../assets/random_thumbnail.jpg';
import {useState} from 'react';
import './Video.css';

function Video(props) {

    const [visibleToolTip, setVisibleToolTip] = useState(false);

    const scoreColor = {
        "backgroundColor":  props.videoInfo.category == 'Cannot be verified' ? "#8B0000"        : 
                            props.videoInfo.category == 'Not so Verifiable' ? "	#FF8C00"     : 
                            props.videoInfo.category == 'Somewhat Verifiable' ? "#8B8000"    :
                            props.videoInfo.category == 'Verifiable' ? "#008B8B"  :
                            props.videoInfo.category == 'Very Verifiable' ? "#006400" : "black"
    } 

    const backgroundColor = {
        "backgroundColor":  props.toggled ? "blue" : null
    }

    const opacity = {
        "opacity":  1
    } 

    function viewCount(value) {
        const newValue = value.toString()
        let returnable = ""
        if(newValue.length < 4) {
            return newValue + " views"
        } else if(newValue.length < 7) {
            for(let i = 0; i <= parseInt(newValue.length) - 4; i++) {
                returnable = returnable + newValue[i]
            }

            return returnable + "K views"
        } else if(newValue.length < 10) {
            for(let i = 0; i <= parseInt(newValue.length) - 7; i++) {
                returnable = returnable + newValue[i]
            }

            return returnable + "M views"
        } else {
            for(let i = 0; i <= parseInt(newValue.length) - 10; i++) {
                returnable = returnable + newValue[i]
            }
            return returnable + "B views"
        }
    }

    return (
        <div className="video" onClick={props.onClick} style={backgroundColor}>
            <img className="video_thumbnail" src={props.videoInfo.thumbnail} />
            <div className="metadata">
                <p className="title">{props.videoInfo.video_title}</p>
                <p className="view_count">{viewCount(props.videoInfo.view_count)} {props.videoInfo.view_count}<span className="upload_date">{props.videoInfo.video_dop}</span></p>
                <div className="channel_info">
                    <div className='channel_image_wrapper'>
                        <img className='channel_image' src={props.videoInfo.profile} />
                    </div>
                    {props.videoInfo.channel_name}
                    <span className="score" style={scoreColor} onMouseOver={() => setVisibleToolTip(true)} onMouseLeave={() => setVisibleToolTip(false)}>
                        {props.videoInfo.category}
                        { visibleToolTip && 
                            <span className="channel_info_tooltip" style={opacity}> Click the score to learn more!</span>
                        }
                    </span>
                </div>
                <p className="description">{props.videoInfo.description}</p>
            </div>
        </div>
    )
}

export default Video;