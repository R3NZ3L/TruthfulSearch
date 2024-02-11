import random_thumbnail from '../../assets/random_thumbnail.jpg';
import {useState} from 'react';
import './Card.css';
import PropTypes from 'prop-types';

function Card(props) {

    const [visibleModal, setVisibleModal] = useState(false);

    function convertScore() {
        return  props.score == 1 ? "0-19%"  : 
                props.score == 2 ? "20-39%" : 
                props.score == 3 ? "40-59%" :
                props.score == 4 ? "60-79%" :
                props.score == 5 ? "80-100%" : "0-19%"
    }

    const backgroundColor = {
        "backgroundColor":  props.score == 1 ? "red"        : 
                            props.score == 2 ? "orange"     : 
                            props.score == 3 ? "yellow"     :
                            props.score == 4 ? "lightblue"  :
                            props.score == 5 ? "lightgreen" : "black"
    } 

    return (
        <>
        <div className="card">
            <img src={random_thumbnail} />
            <div className="metadata">
                <p className="title">Title</p>
                <p className="view_count">View count<span className="upload_date">Upload Date</span></p>
                <div className="channel_info">
                    <div className='channel_image_wrapper'>
                        <div className='channel_image'>
                            <img src={random_thumbnail} />
                        </div>
                    </div>
                    Channel name 
                    <span className="score" style={backgroundColor} onMouseOver={() => setVisibleModal(true)} onMouseLeave={() => setVisibleModal(false)}>
                        {convertScore(props.score)}
                        { visibleModal && 
                            <span className="channel_info_modal">
                                <p>The channel got a verifiability score of 59% due to these reasons:</p>
                                <p>&#x2022; Has a LinkedIn page</p>
                                <p>&#x2022; Has a Wikipedia page</p>
                                <p>&#x2022; Has a Facebook page</p>
                                <button className="more_info">&#9432; <span className='more_info_text'>Learn More</span></button>
                            </span>
                        }
                    </span>
                </div>
                <p className="description">Trimmed Description</p>
            </div>
        </div>
        </>
    )
}

Card.propTypes = {
    score: PropTypes.number,
}

Card.defaultProps = {
    score: "1",
}

export default Card;