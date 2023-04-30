const append_delete = (li) =>{
    let mark = document.createElement('span');

    let a = document.createElement('a');
    a.setAttribute('href', '#');
    a.setAttribute('onclick', 'delete_website("' + websites[index].name + '", "' + websites[index].url + '")');

    let img = document.createElement('img');
    img.setAttribute('src', '/static/image/trach.svg');

    a.append(img);
    mark.append(a);
    li.appendChild(mark);

    return li;
}

function delete_website(name, weburl){
    let http = new XMLHttpRequest();
    let url = '/websites';
    http.onreadystatechange = () => {
        if(http.readyState === http.DONE){
            if(http.response.error == 0){
                set_msg(http.response.msg, 0);
                set_websites();
            }
            else{
                set_msg(http.response.msg, 1);
            }
        }
    }

    http.open('DELETE', url, true);
    http.responseType = 'json';
    http.setRequestHeader('Content-type', 'application/json');
    http.send(JSON.stringify({'name' : name, 'url' : weburl}));
}