import random_thumbnail from '../../assets/random_thumbnail.jpg';
import {useState} from 'react';
import './Video.css';

function Video(props) {

    const [visibleToolTip, setVisibleToolTip] = useState(false);

    const backgroundColor = {
        "backgroundColor":  props.videoInfo.category == 'Cannot be verified' ? "red"        : 
                            props.videoInfo.category == 'Not so Verifiable' ? "orange"     : 
                            props.videoInfo.category == 'Somewhat Verifiable' ? "yellow"     :
                            props.videoInfo.category == 'Verifiable' ? "cyan"  :
                            props.videoInfo.category == 'Very Verifiable' ? "limegreen" : "black"
    } 

    const opacity = {
        "opacity":  1
    } 

    return (
        <div className="video" onClick={props.onClick}>
            <img className="video_thumbnail" src={random_thumbnail} />
            <div className="metadata">
                <p className="title">{props.videoInfo.video_title}</p>
                <p className="view_count">{props.videoInfo.view_count}<span className="upload_date">{props.videoInfo.video_dop}</span></p>
                <div className="channel_info">
                    <div className='channel_image_wrapper'>
                        <div className='channel_image'>
                            <img src={random_thumbnail} />
                        </div>
                    </div>
                    {props.videoInfo.channel_name}
                    <span className="score" style={backgroundColor} onMouseOver={() => setVisibleToolTip(true)} onMouseLeave={() => setVisibleToolTip(false)}>
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