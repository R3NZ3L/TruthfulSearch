const res = fetch('http://127.0.0.1:105/returnmesomedata?name=covidCNN&name2=1&name3=testingtesting', {
    method: 'GET',
}).then(response => {
    if(response.status == 200){
        return response.json();
    } else {
       console.log("failed getting response")
    }
}).then(json => {
    console.log('Success! ' + JSON.stringify(json))
}).catch(error => {
    console.log('error with access token req!')
})
