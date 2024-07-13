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
            <div id="score-container">
                <span id="verifiability-score">
                    ${data.category}
                </span>
            </div>
            <h1 class="video-title">${data.video_title}</h1>
            <div class="channel-numbers">
            <div>
                <h2>${valueCount(data.sub_count)}</h2>
                <h2>Subscribers</h2>
            </div>
            <div>
                <h2>${valueCount(data.like_count)}</h2>
                <h2>Likes</h2>
            </div>
            <div>
                <h2>${valueCount(data.comment_count)}</h2>
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
            <h1>Sources:</h1>
            <div class='link-icon-container'>
            ${data.Website ?
                `<a class='link-icon-URL' href=${fixURL(data.Website)}>
                    <img class="link-icon" src="https://cdn-icons-png.freepik.com/256/1006/1006771.png"></img>
                </a>`: ``}
            ${data.Wiki ?
                `<a class='link-icon-URL' href=${fixURL(data.Wiki)}>
                    <img class="link-icon" src="https://en.wikipedia.org/static/images/icons/wikipedia.png"></img>
                </a>`: ``}
            ${data.LinkedIn ?
                `<a class='link-icon-URL' href=${fixURL(data.LinkedIn)}>
                    <img class="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACtklEQVR4AeyVA5AkQRREZ862bTMcZ9u2wzrbtm3bWNvmaW3b3rzKRa+NOWVEDoqvqv//LZPtUpoubC2cLIxKMveyku1UmkYAG2EoyFYESFEgQIos346dX7K7YiFyN8iFB17Sxx4NRxzVdcbYO6aotke5cgB42sFXDGDjF4FM+UbGY+5TK9FXKQBKOKTtjNz68CMAdQ+oVjyAXPicoRtyS8M5GA0PqRGwgm9gxxdMf2SBkNhEZCoxORXbVH9CXllBWHOvCla9sQNPbegRit3qDmhyWL1SYkCKA7kIxvoH1MBrr5KZllJ/IWnK3zskZ/SXEIDB1vm0trAO6K5ndNCYN5DRz9tgWxdhfnc8pQ2madXdSmDb7CeWWPfOHite22LoDWMegiDFj4GJ983hFBLD9IOPcEB0AjZ8+S6daIeaAwJFG/v8ouJh4ROB3uf1sFHpB34GRSMmMRlJKalISE5hLEHJIRCjbptAXlyAmY8tEZ2QjOzaK4qSbHs6AItTdhHwvpU3N0ZB+hYQhcGXDTi//AFSUtNPW5SY3lX3KJc7gKSwuESYeIXByDMM4XFJyC1bv0i0PKbJoCx/ALewWMwSwccApZe9skFwTAKyiXEjPYZyBziq48zUlVK09j4VvLL3Q3ZFxCdh/D0z7lG+AHFJKVj03DrHwhxHqOzimjMeWZQ/QKQ42ZQH5jkW5u896o7IJmYJa0T5A/BqJ+S6Wv7eqebwH+A/QOUBTMwHYFdpAaY9tACrVqyYECPMOr9d1UF6Gx7QcgLb2McxfCOOu2uaB2CLyk/EJ6WPo4PEmtOLqgOsZK2Pa4IDSUvPeWKFXud1pRre94Ie5jy1kvqnC+AWxzTYn2Odnud0MSdjDM0i1ObXOvDVBQjNEFciMJrhKHJwH5FmDgIPfNds4DuniO75P3r6HNY9BwATNI1Cu+uNpgAAAABJRU5ErkJggg=="></img>
                </a>`: ``}
            ${data.Twitter ?
                `<a class='link-icon-URL' href=${fixURL(data.Twitter)}>
                    <img class="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAAAAABWESUoAAABhUlEQVR4AczOA6xcARCF4X/us23btuLUQR3WZlhbQW3bto2gtm3b2J3GN4tY74uHh3okOi42Nj4AAUDwTvDEhisABCOAEAzYTBh0bN+lc5d0QgAhHPqX4Y4pkd367Zc+xMcXCPDg8TPwxeQH724Uj9N95GJ4pnHxby1xgCmV3v+GsFb7k0Iee7UjaQgmIYe9v9O4+wUKWaATyMPAViwvr1NnOQWDdTV5CHYSaKWLmaGDyvU4mTgQcllracaFr+9uk+yLM8k8fAJff0IUTghRVFu3M1ynkYk4nchiqqU3Ry05RDibMMhjtj6Ht3dJxVk/l1G64cspOusychBsCWm01WNM0jFs0sbEYUtIIuTXNco588OLh09JxE6wweuXEAvfL9PQus3+iU80N34KCaQyUOcxTTuSjEmMRI5rS9JwIZfD1t7ceo34YIpnuQ4nGwP8XXlq/fJZd9jE8KBHC5IwAELJ7dWrZ6fOuNhkgFgAEEIAwA1MQkw0AgDC/wnKycrKSQ2iPAkAVyNzq8rxicIAAAAASUVORK5CYII="></img>
                </a>`: ``}
            ${data.Facebook ? 
                `<a class='link-icon-URL' href=${fixURL(data.Facebook)}>
                    <img class="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAA1UlEQVR4AWOwDp9LUzTELRi1wDdtaf+8w9sPXDtx7h4Q7Tt2c92OS9SxwCZibtesg0+fv3756i0aoo4FkxcdgxhHEwtiite8ePmGhhas3HIB2cRL1x5t3HV5xebzEEQFC67efAI3/cDxW7aR86icip6/QIRP9+xD1E+myOHTPv3AqAVA1DJ1/76jN+EI2YKLVx8hS+0+cgMY5yRbMHfVKbBxhNGFqw+B6mloweY9V2hrAbAIIceCugl7gE6DI2QTT124jyyVXrNxEKaiUQtGLRi1YNQCAMs01I34bbYCAAAAAElFTkSuQmCC"></img>
                </a>`: ``}
            ${data.Instagram ? 
                `<a class='link-icon-URL' href=${fixURL(data.Instagram)}>
                    <img class="link-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAKS0lEQVR4AZ2UA5RkS7ZA94mIq8ys6
                    mrb7v7PGNu2bdu2bdvssZ9trme03V1VWZWZFxFxfv5a41n6s8/al2EJ/Ccve8P566a78YSF6+Ys745PLW2bbA42LSQQbFQVNWJjUKIniRZRkOiNiSImqiRirdZ+YLNkl4Hbx
                    vdOTnSS7CbgGv4N+ehTLuFvjK+IW6/faT/nPfeAlEG3ouUcje9jYsAhmCgkUTExIgquAadgQ8QEcDFim4ioINFgsbRahlgGMPGizfdY9Lx/boh892XXAXCl7HzktVeNbUvzhC
                    JTUtNgQwQFh5JKQNQgPpLEgFOQCDYG0iCYAAaP/duIeMBHiIpEwUQIA5jqKusfMu/RwDYA5yf7zH90cuyN781/PtI2jJg+Ogg4DSQGRJXqkKc3WSJ1iYlg1cw0wkbFhIBvFIvB
                    xohDEAxZO6G9IEfEEGsQY7GFkAw8+3974OcP/uwxJwOXyWl/uCn/9Zf3f/32K6onLVlt0SZgRUmc4eitk8TxktX/M8qCFW06bcElCUbMTMUOj0TFqMEOVQ/BN9TdQG97j0PXj
                    lNkKWOrRmh8RFWwScLE7QNGThz95aanLHqm23fN3gf0dvQetXA0IeuVGCAxhv0X72PtsW0e99W7svm+K/hvuO203Zz72gvoXrmPuWvm4xUolblzDH7X4CGDm/v3czecOXVHM9C
                    8VUSSKpJnjn0X7+Buj1rGc37yYAAgcPC6w/T2l2it4BUNEdUIgBGLNYKkik0c2dI28zbOZc19lrHmisfxu8f9il0/3c2c1YsI2oATTO2d3xmOcWHCLO/EmrSJpAambhxn6yljw
                    8ofBMBl37mCC999KdWeAdIEbIyYqFgEiFgiZiaY0TrLtJ+goMOdv/FQNjxzCw/6yUP55ak/oHfJEVorRolRQRWO9DuOXjdr2QTnA84Gku44937ZKYBw3U+v4cdP/wlLs7nMX9T
                    G/q1Ca3ABpO8BJckcKgbjoTrSZ+2jTqTf7/OHZ30Vlz+fNU/cxJZXHsuFT/kTrilQI2hUqJrcdZw2sazIBOrD0yxb3+aYJ20C4OJPnMuqZJQFK1uEqiRxFlMr5a79VLEkT9uIC
                    r2mpDAZTTQseuQW7vTzRwIgD6y47IU/Hzbgzax98mZufsNF6KEedl5OJGLKsnCZjbVvarJUaCammbd+HohhfPshwnVHmTs/w1Q9cmvx3S6DQ/tYfq8trHzBnRk5dhFGDUev2c/
                    Or1zIntPOJx5dxN9ouZSJyUl6uyZoLx+jWJHT232IRHMQkEHpXBJrmTlMiORNn86oAFDvmyQru2QjYzgnMDVNPHSAO33pCax8/j35Z0a2LGDlE47llq8ew1XP+wbnn/ppGG3TO2
                    M3Hdei2tWdaUA6x9GnxEpFULBk0RUmaDQlmUSiluS5AEAIZFRktsGqoXdwByd+7okzlQcN3Pbh3zLx6+sRNcx+2DGsfsP9WffcO2Gk4prnfolRVtGZPUZvfAppIgBpKlgaTPQYF
                    YxRnKNBhuYEIn0y6wGQGEkZvict/I7DrHjAZla++AEAXPGgD3DkjxdTsAgQDp5/PhNnXMdJf3w1a55zTw7/+EqqP+1EbENCjcQAgBWPxWOQmXuiDSbVmlRKclvTTnokpgRAYiA3
                    FWk6IKkPsfRxJwBw2yd/SvePp7FwzQY6a0fprB5l6bL1HP3TWWz/2O8BWPKYU/B0MRpQPBoDAKIRS42RCoOCCqZIBhRuQD40G5raGgBBaaU9cp2imG/pnLwGgMGZFzO7NYrJexg
                    zjWOAcQ2jtOmddiUA7TsuJ0lybF1hqCAoAFbAILgQMTSoqXFJUmKykiz12KJPkg0AcK4mb0+RFQWmPQAbAXC2gqzEpCUIIA3ESGoHWAYAiAacGb7TwhEQUQCiRoSAAVwMmOjFZE
                    mlrbSkyIe2+qRZBYDYSNoevo9WuGYf1XXXATB6r+PR8ZvJWgFXeGyrweUVMewY/tsKQP+i25CqiysEQwPmbyPQYKhBAkbBKZhWVtFKB2T50GKKNK0BkBTSTp+kKMnnw9QffwnAw
                    pc+i/aT701z8R/h4PVDb6Z/7WmM3e8uLHndEwA4+tMzyQC1FZaAEQHAEf/6HlCJKKjLskpdMY0rFNupsGkJgE2EZNSTtAZkmxZRXX4a4z/6NrOf8HRWfPuLTNzlJMozLiB6YezO
                    z2H+K54NwK7PbyP8+RyKNZvwZYUxATEAEBUEjxARiagEXDLTgAFpITDaYG2Xv41AMlLjWh4c5BsWM/WZN2ELx+jDn8zcF78Ihv4zB765jalXfIjOyqWEVDF1RG2DJgaAWFUIAVG
                    PiGBiFDcccrGFx+UR02mwOgmAzJ6NG1Nc0UddgnRaJK0l9D/xcspzfkv7QU8lXb0OwVLefBPj3/0p1a/OZmTLWnxeoN0S1JAUgls0C4A4MY3BAQGDRQji0lk+Gh1giwQ3p4XWB1
                    AgW7iWZPkCzMHtyLx10NRI0cHO20q98zy6H/oLks9Fa0PYNwlmhNadNxBLh+kNkJEO5d49ZGtX0Fq7kAaIu46QpCmqEQmKyRNvJPdl0VayvCFZ1Eamb2Fw2S8xQPG41+D9Lky5A
                    zOimKLBtAPpptWkJ2wkWTmbdPkYxYnrybYsQ/IKSRvIa8LeG6m6tzL/DU8BGJ6OZw0bvp1kLEeiMhNOS2dmtyuJ+3GZhdyQaoG/4MvoSY9g5PhHYF7xU8JZn0F7ByAGCAGpA6YU
                    tInERpCBQB/ilCP2UqgK7JIlLHv/25j7hHvRAAc+8UtyCsSB8QExlqTtKhfNYMJkBjsimBTMnA1w8Bp6215K61GfpX38Y4j/5+GboXeI2FSY4JGgRB/RoBANUQVCgpJgZi8gXb8
                    BEYjAbY9/J3rh1aRrjiNUHoxDiUQ1U7L3L194ZHbVth+mWmbMakPqsNYQjt4AS48hvdNrSRbfAeH/hwLTZ1/A/jd/gfqC20g3HUPVd0Sf4AcJTXRh7DEnPEV2XXNOkl79na+OHLn
                    y6TpvBSYJqLOYNIPpXcRQI3M3Q3sRalsIDhOE6APa+KEKZYAKfKnEbo0emqJ/2z4GF92OjbOIi9fgJxJ8PwEpmN4xgTlu/e9XvOCBz5D9X7ySsOHCjbMObLsycXmunTHUKeIcuAS
                    LEMtx1E+hIYKfkVh7pFRi3xMHDaHXQFfxk4HQBa1nEdwCwnRCM2Hw/QzftAlHIoPJmlXvecEdgYscwxd7yYk3Du42/Zjk6AW/NXlAkwKxBdFCNALFUmQmgBARHyB4qCK2CpiywfRq
                    dNpjpiN+WglHFR0XmiqimUOqiJ0c0J/wdJ5x78cfvvm6iwDsM1fdhf7RQ/SuaN3cvv/yHzrbbCLL1pgsw1mBNAFrcFYxBowoGMVqRPCICUio/2oDTY0MamK/JDQRug1EhzYpfZ9dy
                    F23PNT3B6cPZShy6SM/xr+z9eNz15h49BjaYwu08R2QZUI6V4lNDF5M8GgIaipvY+2T0NRo6SX2gml6lQ3TTWbLfNztnTw0befvqa+fODDIxq4Cruff+F/YMSYOvVvlzAAAAABJRU
                    5ErkJggg=="></img>
                </a>`: ``}
            </div>
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
                <td>Website Backlinks</td>
                <td>${data.we_desc}</td>
                </tr>
                <tr>
                <tr>
                <td>Wikipedia Backlinks</td>
                <td>${data.wi_desc}</td>
                </tr>
                <td>LinkedIn Backlinks</td>
                <td>${data.li_desc}</td>
                </tr>
                <tr>
                <td>Twitter/X Backlinks</td>
                <td>${data.tw_desc}</td>
                </tr>
                <tr>
                <td>Facebook Backlinks</td>
                <td>${data.fb_desc}</td>
                </tr>
                <tr>
                <td>Instagram Backlinks</td>
                <td>${data.insta_desc}</td>
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
        const parent = document.getElementById("secondary")
        const node = document.createElement("div")
        node.setAttribute("id", "secondary-card");
        node.innerHTML = card;
        parent.insertBefore(node, parent.firstChild);
        colors = {
            'Cannot be verified': '#8B0000', 
            'Not so Verifiable': '#FF8C00', 
            'Somewhat Verifiable': '#8B8000', 
            'Verifiable': '#008B8B', 
            'Very Verifiable': '#006400'
        }
        element = document.getElementById('verifiability-score');
        element.style.backgroundColor = colors[element.innerText]; // set color depending on the verifiability category.
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
    fetch("https://truthful-search-back-end.vercel.app/api/data_extension?id=" + currentParams.get('v')) // get data of current video
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

/* Dynamic changing of values when wanted

const comments_observer = new MutationObserver(() => { // updates the comment count after the user scrolls down to the comment section
    if(document.getElementById('leading-section')) {
        comments_observer.disconnect();
        if (document.getElementById('dynamic-comments') != null) {
            document.getElementById('dynamic-comments').innerText = document.getElementById('leading-section').getElementsByClassName('style-scope yt-formatted-string')[0].innerText;
        }
    }
});

const likes_sub_observer = new MutationObserver(() => { // updates the subscriber and like count
    if(document.getElementById('top-row')) {
        likes_sub_observer.disconnect();
        document.getElementById('dynamic-subs').innerText = document.getElementById('owner-sub-count').innerText.split(" ")[0];
        document.getElementById('dynamic-likes').innerText  = document.getElementsByClassName('YtLikeButtonViewModelHost')[0].getElementsByClassName('yt-spec-button-shape-next__button-text-content')[0].innerHTML;
    }
});

comments_observer.observe(document.body, { // Check if the comment section already loaded
    subtree: true,
    childList: true,
});

likes_sub_observer.observe(document.body, { // Check if the comment section already loaded
    subtree: true,
    childList: true,
});

*/