import './InfoCard.css'

function InfoCard(props) {
    return (
        <div className="card">
            <div className="img1"><img src="https://play-lh.googleusercontent.com/zaMefYVID82FrctnM3g2b9Ul1Wk9cAR1aYfKNq_uvHnDbGo2wqZgliYVioi8Fa3YTA" /></div>
            <div className="img2"><img src="https://play-lh.googleusercontent.com/zaMefYVID82FrctnM3g2b9Ul1Wk9cAR1aYfKNq_uvHnDbGo2wqZgliYVioi8Fa3YTA" /></div>
            <div className="main-content">
              <div className="details">
                <h2>{props.video.channel_name}</h2>
                <h1>{props.video.video_title}</h1>
                <div className="channel-numbers">
                  <div>
                    <h2>{props.video.sub_count}</h2>
                    <h2>Subscriber</h2>
                  </div>
                  <div>
                    <h2>{props.video.like_count}</h2>
                    <h2>Likes</h2>
                  </div>
                  <div>
                    <h2>{props.video.comment_count}</h2>
                    <h2>Comments</h2>
                  </div>
                </div>
              </div>
              
              <div className="channel-information">
                <div className="channel-links">
                  <h1>Profile Links:</h1>
                  {props.video.Facebook &&<span>Facebook: <u><a href={props.video.Facebook}>{props.video.Facebook}</a></u></span>}
                  {props.video.LinkedIn && <span>LinkedIn: <u><a href={props.video.LinkedIn}>{props.video.LinkedIn}</a></u></span>}
                  <span>Other websites associated with the content creator:</span>
                  <ul>
                    {props.video.Wiki &&  <li>Wikipedia: <u><a href={props.video.Wiki}>{props.video.Wiki}</a></u></li>}
                    {props.video.Twitter &&  <li>Twitter: <u><a href={props.video.Twitter}>{props.video.Twitter}</a></u></li>}
                    {props.video.Website &&  <li>Personal: <u><a href={props.video.Website}>{props.video.Website}</a></u></li>}
                  </ul>  
                </div>
              </div>

              <div className="video-score-breakdown">
                <table>
                  <thead>
                    <tr>
                      <th colSpan="2">Verifiability Score Breakdown</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Profiles (LinkedIn, Facebook, and Twitter/X)</td>
                      <td>10%</td>
                    </tr>
                    <tr>
                      <td>External Sites (Wikipedia and other Websites)</td>
                      <td>10%</td>
                    </tr>
                    <tr>
                      <td>Backlinks (LinkedIn)</td>
                      <td>10%</td>
                    </tr>
                    <tr>
                      <td>Backlinks (Facebook)</td>
                      <td>10%</td>
                    </tr>
                    <tr>
                      <td>Backlinks (Twitter/X)</td>
                      <td>10%</td>
                    </tr>
                    <tr>
                      <td>Backlinks (Wikipedia)</td>
                      <td>10%</td>
                    </tr>
                    <tr>
                      <td>Backlinks (Other Websites)</td>
                      <td>10%</td>
                    </tr>
                  </tbody>
                  <tfoot>
                    <tr>
                      <td>Total</td>
                      <td>100%</td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </div>
    )
}

export default InfoCard;