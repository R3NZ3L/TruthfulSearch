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

function template(data) { 
    return `<div class="card">
        <div class="img2"><img src=${data.profile} /></div>
        <div class="main-content">
        <div class="details">
            <h2 class="channel_name">${data.channel_name}</h2>
            <h1>${data.video_title}</h1>
            <div class="channel-numbers">
            <div>
                <h2>${document.getElementById('owner-sub-count').innerText.split(" ")[0]}</h2>
                <h2>Subscriber</h2>
            </div>
            <div>
                <h2>${document.getElementsByClassName('YtLikeButtonViewModelHost')[0].getElementsByClassName('yt-spec-button-shape-next__button-text-content')[0].innerHTML}</h2>
                <h2>Likes</h2>
            </div>
            <div>
                <h2 id="comment_count">0</h2>
                <h2>Comments</h2>
            </div>
            <div>
                <h2>${data.backlinks}</h2>
                <h2>Video Cited By</h2>
            </div>
            </div>
        </div>
        
        <div class="channel-information">
            <div class="channel-links">
            <h1>Related Links:</h1>
            <ul>
            ${true ? 
                `<li>
                    <span class="link-item-container">
                        <img class="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAA1UlEQVR4AWOwDp9LUzTELRi1wDdtaf+8w9sPXDtx7h4Q7Tt2c92OS9SxwCZibtesg0+fv3756i0aoo4FkxcdgxhHEwtiite8ePmGhhas3HIB2cRL1x5t3HV5xebzEEQFC67efAI3/cDxW7aR86icip6/QIRP9+xD1E+myOHTPv3AqAVA1DJ1/76jN+EI2YKLVx8hS+0+cgMY5yRbMHfVKbBxhNGFqw+B6mloweY9V2hrAbAIIceCugl7gE6DI2QTT124jyyVXrNxEKaiUQtGLRi1YNQCAMs01I34bbYCAAAAAElFTkSuQmCC"></img> 
                        <div class="link-item">
                            <span class="link-name">Facebook (Cited by: ${data.Facebook_backlink_count} webpages)</span>
                            <a href=${fixURL(data.Facebook)} target="_blank">${data.Facebook}</a>
                        </div>
                    </span>
                </li>`: ``}
            ${true ?
                `<li>
                <span class="link-item-container">
                <img class="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAAAAABWESUoAAABhUlEQVR4AczOA6xcARCF4X/us23btuLUQR3WZlhbQW3bto2gtm3b2J3GN4tY74uHh3okOi42Nj4AAUDwTvDEhisABCOAEAzYTBh0bN+lc5d0QgAhHPqX4Y4pkd367Zc+xMcXCPDg8TPwxeQH724Uj9N95GJ4pnHxby1xgCmV3v+GsFb7k0Iee7UjaQgmIYe9v9O4+wUKWaATyMPAViwvr1NnOQWDdTV5CHYSaKWLmaGDyvU4mTgQcllracaFr+9uk+yLM8k8fAJff0IUTghRVFu3M1ynkYk4nchiqqU3Ry05RDibMMhjtj6Ht3dJxVk/l1G64cspOusychBsCWm01WNM0jFs0sbEYUtIIuTXNco588OLh09JxE6wweuXEAvfL9PQus3+iU80N34KCaQyUOcxTTuSjEmMRI5rS9JwIZfD1t7ceo34YIpnuQ4nGwP8XXlq/fJZd9jE8KBHC5IwAELJ7dWrZ6fOuNhkgFgAEEIAwA1MQkw0AgDC/wnKycrKSQ2iPAkAVyNzq8rxicIAAAAASUVORK5CYII="></img>
                <div class="link-item">
                    <span class="link-name">X-(Twitter) (Cited by: ${data.Twitter_backlink_count} webpages)</span>
                    <a href=${fixURL(data.Twitter)} target="_blank">${data.Twitter}</a>
                </div>
                </span></li>`: ``}
            ${true ?
                `<li>
                <span class="link-item-container">
                <img class="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACtklEQVR4AeyVA5AkQRREZ862bTMcZ9u2wzrbtm3bWNvmaW3b3rzKRa+NOWVEDoqvqv//LZPtUpoubC2cLIxKMveyku1UmkYAG2EoyFYESFEgQIos346dX7K7YiFyN8iFB17Sxx4NRxzVdcbYO6aotke5cgB42sFXDGDjF4FM+UbGY+5TK9FXKQBKOKTtjNz68CMAdQ+oVjyAXPicoRtyS8M5GA0PqRGwgm9gxxdMf2SBkNhEZCoxORXbVH9CXllBWHOvCla9sQNPbegRit3qDmhyWL1SYkCKA7kIxvoH1MBrr5KZllJ/IWnK3zskZ/SXEIDB1vm0trAO6K5ndNCYN5DRz9tgWxdhfnc8pQ2madXdSmDb7CeWWPfOHite22LoDWMegiDFj4GJ983hFBLD9IOPcEB0AjZ8+S6daIeaAwJFG/v8ouJh4ROB3uf1sFHpB34GRSMmMRlJKalISE5hLEHJIRCjbptAXlyAmY8tEZ2QjOzaK4qSbHs6AItTdhHwvpU3N0ZB+hYQhcGXDTi//AFSUtNPW5SY3lX3KJc7gKSwuESYeIXByDMM4XFJyC1bv0i0PKbJoCx/ALewWMwSwccApZe9skFwTAKyiXEjPYZyBziq48zUlVK09j4VvLL3Q3ZFxCdh/D0z7lG+AHFJKVj03DrHwhxHqOzimjMeWZQ/QKQ42ZQH5jkW5u896o7IJmYJa0T5A/BqJ+S6Wv7eqebwH+A/QOUBTMwHYFdpAaY9tACrVqyYECPMOr9d1UF6Gx7QcgLb2McxfCOOu2uaB2CLyk/EJ6WPo4PEmtOLqgOsZK2Pa4IDSUvPeWKFXud1pRre94Ie5jy1kvqnC+AWxzTYn2Odnud0MSdjDM0i1ObXOvDVBQjNEFciMJrhKHJwH5FmDgIPfNds4DuniO75P3r6HNY9BwATNI1Cu+uNpgAAAABJRU5ErkJggg=="></img> 
                <div class="link-item">
                    <span class="link-name">LinkedIn (Cited by: ${data.LinkedIn_backlink_count} webpages)</span>
                    <a href=${fixURL(data.LinkedIn)} target="_blank">${data.LinkedIn}</a>
                </div>
                </span></li>`: ``}
            ${true ?
                `<li>
                <span class="link-item-container">
                <img class="link-icon" src="https://cdn-icons-png.flaticon.com/512/3858/3858448.png"></img> 
                <div class="link-item">
                    <span class="link-name">Personal (Cited by: ${data.Website_backlink_count} webpages)</span>
                    <a href=${fixURL(data.Website)} target="_blank">${data.Website}</a>
                </div>
                </span></li>`: ``}
            ${true ?
                `<li>
                <span class="link-item-container">
                    <img class="link-icon" src="https://en.wikipedia.org/static/images/icons/wikipedia.png"></img> 
                    <div class="link-item">
                        <span class="link-name">Wikipedia (Cited by: ${data.Wiki_backlink_count} webpages)</span>
                        <a href=${fixURL(data.Wiki)} target="_blank">${data.Wiki}</a>
                    </div>
                </span></li> `: ``}
            </ul> 
            </div>
        </div>
        
        <div class="video-score-breakdown">
            <table>
            <thead>
                <tr>
                <th colSpan="2">Verifiability Breakdown</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                <td>Profiles (LinkedIn, Facebook, and Twitter/X)</td>
                <td>${data.p_desc}</td>
                </tr>
                <tr>
                <td>External Sites (Wikipedia and other Websites)</td>
                <td>${data.e_desc}</td>
                </tr>
                <tr>
                <td>LinkedIn Backlinks</td>
                <td>${data.li_desc}</td>
                </tr>
                <tr>
                <td>Facebook Backlinks</td>
                <td>${data.fb_desc}</td>
                </tr>
                <tr>
                <td>Twitter/X Backlinks</td>
                <td>${data.tw_desc}</td>
                </tr>
                <tr>
                <td>Wikipedia Backlinks</td>
                <td>${data.wi_desc}</td>
                </tr>
                <tr>
                <td>Website Backlinks</td>
                <td>${data.we_desc}</td>
                </tr>
            </tbody>
            </table>
        </div>
        </div>
    </div>`
}

let card = null
function loadCard() {
    if (card != null) {
        document.getElementById('secondary-inner').style.display = 'none';
        const node = document.createElement("div")
        node.setAttribute("id", "secondary-card");
        node.innerHTML = card;
        document.getElementById("secondary").appendChild(node);
    }
}

const recommendation_bar_observer = new MutationObserver(() => {
    if(document.getElementById('secondary-inner')) {
        recommendation_bar_observer.disconnect();
        loadCard()
    }
});

var currentURL = window.location.search;
var currentParams = new URLSearchParams(window.location.search);
function loadData(state) {
    fetch("http://127.0.0.1:105/api/data_extension?id=" + currentParams.get('v')) // get data of current video
    .then(response => {
        if (response.status == 200) return response.json()
        else if (response.status == 404) throw 'Data not found in the database'
        else if (response.status == 500) throw 'Database Error'
    })
    .then(data => {
        console.log('Video found in the database')
        card = template(data);
        if (state == 'initial') {
            recommendation_bar_observer.observe(document.body, {
                subtree: true,
                childList: true,
            });
        } else if (state == 'changevideo') {
            if (document.getElementById('secondary-card') != null) {
                document.getElementById('secondary-card').remove()
            }
            loadCard()
        }
    }).catch((error) => {
        console.log('Error: ' + error)
        if (document.getElementById('secondary-card') != null) {
            document.getElementById('secondary-card').remove()
            document.getElementById('secondary-inner').style.display = 'block';
            card = null
        }
    });
}

window.addEventListener("load", () => {
    loadData('initial');
    console.log('Initial load of the document/window')
});

var videoElement = document.querySelector('video');
videoElement.addEventListener('canplay', function(event) {
    var newURL = window.location.search
    if(currentURL != newURL) {
        currentURL = newURL;
        currentParams = new URLSearchParams(newURL);
        loadData('changevideo');
    }
});

const comments_observer = new MutationObserver(() => { // updates the comment count after the user scrolls down to the comment section
    if(document.getElementById('leading-section')) {
        comments_observer.disconnect();
        if (document.getElementById('comment_count') != null) {
            document.getElementById('comment_count').innerText = document.getElementById('leading-section').getElementsByClassName('style-scope yt-formatted-string')[0].innerText;
        }
    }
});

comments_observer.observe(document.body, { // Check if the comment section already loaded
    subtree: true,
    childList: true,
});

/*
document.getElementsByClassName('ytp-next-button ytp-button')[0].addEventListener('click', function () { // when next button is clicked
    loadData('changevideo');
    console.log('The user clicked the next video button')
});

document.getElementsByClassName('ytp-prev-button ytp-button')[0].addEventListener('click', function () { // when previous button is clicked
    loadData('changevideo');
    console.log('The user clicked the previous video button')
});

window.addEventListener('popstate', function () { // When the user goes back or forward using the browser's history
	loadData('changevideo');
    console.log('The user goes back or forward using the browser\'s history')
});
*/

