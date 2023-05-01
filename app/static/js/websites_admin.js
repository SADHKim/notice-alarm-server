function delete_website(website){
    let http = new XMLHttpRequest();
    let url = '/websites';

    http.onreadystatechange = () => {
        if(http.readyState === http.DONE){
            if(http.response.error == 0){
                set_msg(http.response.msg, 0);
            }
            else{
                set_msg(http.response.msg, 1);
            }
        }
    }

    http.open('DELETE', url, true);
    http.responseType = 'json';
    http.setRequestHeader('Content-type', 'application/json');
    http.send(JSON.stringify({'name' : website}));
}