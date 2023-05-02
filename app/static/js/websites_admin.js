function delete_website(website){
    let http = new XMLHttpRequest();
    let url = '/websites';

    http.onreadystatechange = () => {
        if(http.readyState === http.DONE){
            if(http.response.error == 0){
                location.reload(true);
            }
            else if (http.response.error == -1){
                alert(http.response.msg);
            }
        }
    }

    http.open('DELETE', url, true);
    http.responseType = 'json';
    http.setRequestHeader('Content-type', 'application/json');
    http.send(JSON.stringify({'name' : website}));
}