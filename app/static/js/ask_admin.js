function delete_ask(url){
    let http = new XMLHttpRequest();
    let api_url = '/api/asks';
    http.onreadystatechange = () => {
        if(http.readyState === http.DONE){
            if(http.response.error == 0){
                location.reload(true)
            }
            else if (http.response.error == 1){
                alert(1)
            }
            else{
                alert(http.response.msg)
            }
        }
    };

    http.open('DELETE', api_url, true);
    http.responseType = 'json';
    http.setRequestHeader('Content-type', 'application/json');
    http.send(JSON.stringify({'url' : url}));
}