const append_delete = (li) =>{
    let span = document.createElement('span');

    let button = document.createElement('a');
    button.setAttribute('href', '#');
    button.setAttribute('onclick', 'delete_ask("' + asks[index].url + '")');

    let img = document.createElement('img');
    img.setAttribute('src', '/static/image/trach.svg');
    
    button.append(img);
    span.append(button);
    li.append(span)

    return li;
}

function delete_ask(url){
    let http = new XMLHttpRequest();
    let api_url = '/api/asks';
    http.onreadystatechange = () => {
        if(http.readyState === http.DONE){
            if(http.response.error == 0){
                set_msg(http.response.msg, 0);
                set_asks();
            }
            else{
                set_msg(http.response.msg, 1);
            }
        }
    };

    http.open('DELETE', api_url, true);
    http.responseType = 'json';
    http.setRequestHeader('Content-type', 'application/json');
    http.send(JSON.stringify({'url' : url}));
}