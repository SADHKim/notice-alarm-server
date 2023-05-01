function add_website(user, website){
    
    let http = new XMLHttpRequest();
    let url = '/api/websites';
    http.onreadystatechange = () => {
        if(http.readyState === http.DONE){
            if (http.response.error == 0){
                location.reload(true);
            }
            else if(http.response.error == 1){
                alert('you already have the website!')
            }
        }
    }

    http.open('POST', url, true);
    http.responseType = 'json';
    http.setRequestHeader('Content-type', 'application/json');
    http.send(JSON.stringify({'user' : user, 'website' : website}))
}