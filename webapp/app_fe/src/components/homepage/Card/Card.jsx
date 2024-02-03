import random_thumbnail from '../../../assets/random_thumbnail.jpg'
// import profilepicture from '../../../assets/profilepicture.png'
import {useState} from 'react';
import './Card.css'

function Card() {

    const [visibleModal, setVisibleModal] = useState(false)

    const showModal = () => setVisibleModal(true);
    const hideModal = () => setVisibleModal(false);

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
                    <span className="score" onMouseOver={() => setVisibleModal(true)} onMouseLeave={() => setVisibleModal(false)}>
                        59%
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

export default Card;