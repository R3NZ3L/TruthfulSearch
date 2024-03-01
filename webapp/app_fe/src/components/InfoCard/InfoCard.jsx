import './InfoCard.css'

function InfoCard() {
    return (
        <div class="card">
            <div class="img1"><img src="https://play-lh.googleusercontent.com/zaMefYVID82FrctnM3g2b9Ul1Wk9cAR1aYfKNq_uvHnDbGo2wqZgliYVioi8Fa3YTA" /></div>
            <div class="img2"><img src="https://play-lh.googleusercontent.com/zaMefYVID82FrctnM3g2b9Ul1Wk9cAR1aYfKNq_uvHnDbGo2wqZgliYVioi8Fa3YTA" /></div>
            <div class="main-content">
              <div class="details">
                <h2>Channel Name</h2>
                <h1>Video Title</h1>
                <div class="channel-numbers">
                  <div>
                    <h2>12</h2>
                    <h2>Subscriber</h2>
                  </div>
                  <div>
                    <h2>12</h2>
                    <h2>Likes</h2>
                  </div>
                  <div>
                    <h2>12</h2>
                    <h2>Comments</h2>
                  </div>
                </div>
              </div>
              
              <div class="channel-information">
                <div class="channel-links">
                  <h1>Profile Links:</h1>
                  <span>Facebook: <a href="https://www.w3schools.com">www.w3schools.com</a></span>
                  <span>LinkedIn: <a href="https://www.w3schools.com">www.w3schools1.com</a></span>
                  <span>Other websites associated with the content creator:</span>
                  <ul>
                    <li><a href="test.com">test.com</a></li>
                    <li><a href="test.com">test.com</a></li>
                    <li><a href="test.com">test.com</a></li>
                  </ul>  
                </div>
              </div>

              <div class="video-score-breakdown">
                <table>
                  <thead>
                    <tr>
                      <th colspan="2">Verifiability Score Breakdown</th>
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