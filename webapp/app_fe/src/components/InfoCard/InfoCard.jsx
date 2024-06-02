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

  const position = {
    "top":  props.videoPosition,
    "position": "relative"
  }

  
  return (
      <div className="card" style={position}>
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
                <div>
                  <h2>{valueCount(props.video.backlinks)}</h2>
                  <h2>Video Cited By</h2>
                </div>
              </div>
            </div>
            
            <div className="channel-information">
              <div className="channel-links">
                <h1>Related Links:</h1>
                <div className='link-icon-container'>
                  <a className='link-icon-URL' href={fixURL(props.video.Facebook)}>
                    <img className="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAA1UlEQVR4AWOwDp9LUzTELRi1wDdtaf+8w9sPXDtx7h4Q7Tt2c92OS9SxwCZibtesg0+fv3756i0aoo4FkxcdgxhHEwtiite8ePmGhhas3HIB2cRL1x5t3HV5xebzEEQFC67efAI3/cDxW7aR86icip6/QIRP9+xD1E+myOHTPv3AqAVA1DJ1/76jN+EI2YKLVx8hS+0+cgMY5yRbMHfVKbBxhNGFqw+B6mloweY9V2hrAbAIIceCugl7gE6DI2QTT124jyyVXrNxEKaiUQtGLRi1YNQCAMs01I34bbYCAAAAAElFTkSuQmCC"></img>
                  </a>
                  <a className='link-icon-URL' href={fixURL(props.video.Facebook)}>
                    <img className="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAA1UlEQVR4AWOwDp9LUzTELRi1wDdtaf+8w9sPXDtx7h4Q7Tt2c92OS9SxwCZibtesg0+fv3756i0aoo4FkxcdgxhHEwtiite8ePmGhhas3HIB2cRL1x5t3HV5xebzEEQFC67efAI3/cDxW7aR86icip6/QIRP9+xD1E+myOHTPv3AqAVA1DJ1/76jN+EI2YKLVx8hS+0+cgMY5yRbMHfVKbBxhNGFqw+B6mloweY9V2hrAbAIIceCugl7gE6DI2QTT124jyyVXrNxEKaiUQtGLRi1YNQCAMs01I34bbYCAAAAAElFTkSuQmCC"></img>
                  </a>
                  <a className='link-icon-URL' href={fixURL(props.video.Facebook)}>
                    <img className="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAA1UlEQVR4AWOwDp9LUzTELRi1wDdtaf+8w9sPXDtx7h4Q7Tt2c92OS9SxwCZibtesg0+fv3756i0aoo4FkxcdgxhHEwtiite8ePmGhhas3HIB2cRL1x5t3HV5xebzEEQFC67efAI3/cDxW7aR86icip6/QIRP9+xD1E+myOHTPv3AqAVA1DJ1/76jN+EI2YKLVx8hS+0+cgMY5yRbMHfVKbBxhNGFqw+B6mloweY9V2hrAbAIIceCugl7gE6DI2QTT124jyyVXrNxEKaiUQtGLRi1YNQCAMs01I34bbYCAAAAAElFTkSuQmCC"></img>
                  </a>
                  <a className='link-icon-URL' href={fixURL(props.video.Facebook)}>
                    <img className="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAA1UlEQVR4AWOwDp9LUzTELRi1wDdtaf+8w9sPXDtx7h4Q7Tt2c92OS9SxwCZibtesg0+fv3756i0aoo4FkxcdgxhHEwtiite8ePmGhhas3HIB2cRL1x5t3HV5xebzEEQFC67efAI3/cDxW7aR86icip6/QIRP9+xD1E+myOHTPv3AqAVA1DJ1/76jN+EI2YKLVx8hS+0+cgMY5yRbMHfVKbBxhNGFqw+B6mloweY9V2hrAbAIIceCugl7gE6DI2QTT124jyyVXrNxEKaiUQtGLRi1YNQCAMs01I34bbYCAAAAAElFTkSuQmCC"></img>
                  </a>
                  <a className='link-icon-URL' href={fixURL(props.video.Facebook)}>
                    <img className="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAA1UlEQVR4AWOwDp9LUzTELRi1wDdtaf+8w9sPXDtx7h4Q7Tt2c92OS9SxwCZibtesg0+fv3756i0aoo4FkxcdgxhHEwtiite8ePmGhhas3HIB2cRL1x5t3HV5xebzEEQFC67efAI3/cDxW7aR86icip6/QIRP9+xD1E+myOHTPv3AqAVA1DJ1/76jN+EI2YKLVx8hS+0+cgMY5yRbMHfVKbBxhNGFqw+B6mloweY9V2hrAbAIIceCugl7gE6DI2QTT124jyyVXrNxEKaiUQtGLRi1YNQCAMs01I34bbYCAAAAAElFTkSuQmCC"></img>
                  </a>
                </div>
                {/*
                <ul> 
                  <li>{props.video.Facebook && 
                    <span className="link-item-container">
                      <img className="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAA1UlEQVR4AWOwDp9LUzTELRi1wDdtaf+8w9sPXDtx7h4Q7Tt2c92OS9SxwCZibtesg0+fv3756i0aoo4FkxcdgxhHEwtiite8ePmGhhas3HIB2cRL1x5t3HV5xebzEEQFC67efAI3/cDxW7aR86icip6/QIRP9+xD1E+myOHTPv3AqAVA1DJ1/76jN+EI2YKLVx8hS+0+cgMY5yRbMHfVKbBxhNGFqw+B6mloweY9V2hrAbAIIceCugl7gE6DI2QTT124jyyVXrNxEKaiUQtGLRi1YNQCAMs01I34bbYCAAAAAElFTkSuQmCC"></img> 
                      <div className="link-item">
                        <span className="link-name">Facebook (Cited by: {props.video.Facebook_backlink_count} webpages)</span>
                        <a href={fixURL(props.video.Facebook)} target="_blank">{props.video.Facebook}</a>
                      </div>
                    </span>
                  }</li>
                  <li>{props.video.Twitter &&
                    <span className="link-item-container">
                      <img className="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAAAAABWESUoAAABhUlEQVR4AczOA6xcARCF4X/us23btuLUQR3WZlhbQW3bto2gtm3b2J3GN4tY74uHh3okOi42Nj4AAUDwTvDEhisABCOAEAzYTBh0bN+lc5d0QgAhHPqX4Y4pkd367Zc+xMcXCPDg8TPwxeQH724Uj9N95GJ4pnHxby1xgCmV3v+GsFb7k0Iee7UjaQgmIYe9v9O4+wUKWaATyMPAViwvr1NnOQWDdTV5CHYSaKWLmaGDyvU4mTgQcllracaFr+9uk+yLM8k8fAJff0IUTghRVFu3M1ynkYk4nchiqqU3Ry05RDibMMhjtj6Ht3dJxVk/l1G64cspOusychBsCWm01WNM0jFs0sbEYUtIIuTXNco588OLh09JxE6wweuXEAvfL9PQus3+iU80N34KCaQyUOcxTTuSjEmMRI5rS9JwIZfD1t7ceo34YIpnuQ4nGwP8XXlq/fJZd9jE8KBHC5IwAELJ7dWrZ6fOuNhkgFgAEEIAwA1MQkw0AgDC/wnKycrKSQ2iPAkAVyNzq8rxicIAAAAASUVORK5CYII="></img>
                      <div className="link-item">
                        <span className="link-name">X-(Twitter) (Cited by: {props.video.Twitter_backlink_count} webpages)</span>
                        <a href={fixURL(props.video.Twitter)} target="_blank">{props.video.Twitter}</a>
                      </div>
                    </span>
                  }</li>
                  <li>{props.video.LinkedIn && 
                    <span className="link-item-container">
                      <img className="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACtklEQVR4AeyVA5AkQRREZ862bTMcZ9u2wzrbtm3bWNvmaW3b3rzKRa+NOWVEDoqvqv//LZPtUpoubC2cLIxKMveyku1UmkYAG2EoyFYESFEgQIos346dX7K7YiFyN8iFB17Sxx4NRxzVdcbYO6aotke5cgB42sFXDGDjF4FM+UbGY+5TK9FXKQBKOKTtjNz68CMAdQ+oVjyAXPicoRtyS8M5GA0PqRGwgm9gxxdMf2SBkNhEZCoxORXbVH9CXllBWHOvCla9sQNPbegRit3qDmhyWL1SYkCKA7kIxvoH1MBrr5KZllJ/IWnK3zskZ/SXEIDB1vm0trAO6K5ndNCYN5DRz9tgWxdhfnc8pQ2madXdSmDb7CeWWPfOHite22LoDWMegiDFj4GJ983hFBLD9IOPcEB0AjZ8+S6daIeaAwJFG/v8ouJh4ROB3uf1sFHpB34GRSMmMRlJKalISE5hLEHJIRCjbptAXlyAmY8tEZ2QjOzaK4qSbHs6AItTdhHwvpU3N0ZB+hYQhcGXDTi//AFSUtNPW5SY3lX3KJc7gKSwuESYeIXByDMM4XFJyC1bv0i0PKbJoCx/ALewWMwSwccApZe9skFwTAKyiXEjPYZyBziq48zUlVK09j4VvLL3Q3ZFxCdh/D0z7lG+AHFJKVj03DrHwhxHqOzimjMeWZQ/QKQ42ZQH5jkW5u896o7IJmYJa0T5A/BqJ+S6Wv7eqebwH+A/QOUBTMwHYFdpAaY9tACrVqyYECPMOr9d1UF6Gx7QcgLb2McxfCOOu2uaB2CLyk/EJ6WPo4PEmtOLqgOsZK2Pa4IDSUvPeWKFXud1pRre94Ie5jy1kvqnC+AWxzTYn2Odnud0MSdjDM0i1ObXOvDVBQjNEFciMJrhKHJwH5FmDgIPfNds4DuniO75P3r6HNY9BwATNI1Cu+uNpgAAAABJRU5ErkJggg=="></img> 
                      <div className="link-item">
                        <span className="link-name">LinkedIn (Cited by: {props.video.LinkedIn_backlink_count} webpages)</span>
                        <a href={fixURL(props.video.LinkedIn)} target="_blank">{props.video.LinkedIn}</a>
                      </div>
                    </span>
                  }</li>
                  <li>{props.video.Website &&
                    <span className="link-item-container">
                      <img className="link-icon" src="https://cdn-icons-png.flaticon.com/512/3858/3858448.png"></img> 
                      <div className="link-item">
                        <span className="link-name">Personal (Cited by: {props.video.Website_backlink_count} webpages)</span>
                        <a href={fixURL(props.video.Website)} target="_blank">{props.video.Website}</a>
                      </div>
                    </span>
                  }</li>
                  <li>{props.video.Wiki &&
                  <span className="link-item-container">
                      <img className="link-icon" src="https://en.wikipedia.org/static/images/icons/wikipedia.png"></img> 
                      <div className="link-item">
                        <span className="link-name">Wikipedia (Cited by: {props.video.Wiki_backlink_count} webpages)</span>
                        <a href={fixURL(props.video.Wiki)} target="_blank">{props.video.Wiki}</a>
                      </div>
                    </span>
                  }</li>
                </ul>
                */}
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