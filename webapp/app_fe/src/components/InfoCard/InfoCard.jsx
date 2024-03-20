import './InfoCard.css'

function InfoCard(props) {

    function fixURL(url) { 
      if (url.slice(0,8) != 'https://') {
        return 'https://' + url;
      } else {
        return url
      }
    }

    function valueCount(value) {
      const newValue = value.toString()
      let returnable = ""
      if(newValue.length < 4) {
          return newValue
      } else if(newValue.length < 7) {
          for(let i = 0; i <= parseInt(newValue.length) - 4; i++) {
              returnable = returnable + newValue[i]
          }

          return returnable + "K"
      } else if(newValue.length < 10) {
          for(let i = 0; i <= parseInt(newValue.length) - 7; i++) {
              returnable = returnable + newValue[i]
          }

          return returnable + "M"
      } else {
          for(let i = 0; i <= parseInt(newValue.length) - 10; i++) {
              returnable = returnable + newValue[i]
          }
          return returnable + "B"
      }
  }

    return (
        <div className="card">
            <div className="img2"><img src={props.video.profile} /></div>
            <div className="main-content">
              <div className="details">
                <h2 className="channel_name">{props.video.channel_name}</h2>
                <h1>{props.video.video_title}</h1>
                <div className="channel-numbers">
                  <div>
                    <h2>{valueCount(props.video.sub_count)}</h2>
                    <h2>Subscriber</h2>
                  </div>
                  <div>
                    <h2>{valueCount(props.video.like_count)}</h2>
                    <h2>Likes</h2>
                  </div>
                  <div>
                    <h2>{valueCount(props.video.comment_count)}</h2>
                    <h2>Comments</h2>
                  </div>
                </div>
              </div>
              
              <div className="channel-information">
                <div className="channel-links">
                  <h1>Related Links:</h1>
                  <ul> 
                    <li>{props.video.Facebook && <span>Facebook: <u><a href={fixURL(props.video.Facebook)} target="_blank">{props.video.Facebook}</a></u></span>}</li>
                    <li>{props.video.Twitter && <span>Twitter: <u><a href={fixURL(props.video.Twitter)} target="_blank">{props.video.Twitter}</a></u></span>}</li>
                    <li>{props.video.LinkedIn && <span>LinkedIn: <u><a href={fixURL(props.video.LinkedIn)} target="_blank">{props.video.LinkedIn}</a></u></span>}</li>
                    <li>{props.video.Website && <span>Personal: <u><a href={fixURL(props.video.Website)} target="_blank">{props.video.Website}</a></u></span>}</li>
                    <li>{props.video.Wiki && <span>Wikipedia: <u><a href={fixURL(props.video.Wiki)} target="_blank">{props.video.Wiki}</a></u></span>}</li>
                  </ul> 
                </div>
              </div>
              
              <div className="video-score-breakdown">
                <table>
                  <thead>
                    <tr>
                      <th colSpan="2">Verifiability Breakdown</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Profiles (LinkedIn, Facebook, and Twitter/X)</td>
                      <td>{props.video.p_desc}</td>
                    </tr>
                    <tr>
                      <td>External Sites (Wikipedia and other Websites)</td>
                      <td>{props.video.e_desc}</td>
                    </tr>
                    <tr>
                      <td>LinkedIn Backlinks</td>
                      <td>{props.video.li_desc}</td>
                    </tr>
                    <tr>
                      <td>Facebook Backlinks</td>
                      <td>{props.video.fb_desc}</td>
                    </tr>
                    <tr>
                      <td>Twitter/X Backlinks</td>
                      <td>{props.video.tw_desc}</td>
                    </tr>
                    <tr>
                      <td>Wikipedia Backlinks</td>
                      <td>{props.video.wi_desc}</td>
                    </tr>
                    <tr>
                      <td>Website Backlinks</td>
                      <td>{props.video.we_desc}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
    )
}

export default InfoCard;