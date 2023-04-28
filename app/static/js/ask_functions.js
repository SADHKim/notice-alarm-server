var elementAsks;
var asksCnt;
var asks;
var index;

var user = 'guest';
function set_user(id){
    user = id;
}

function open_form(){
    document.getElementById('ask_form').style.display = 'block';
}

window.onload = () => {
    elementAsks = document.getElementById('asks');
    set_asks();
};

function set_asks(){
    let http = new XMLHttpRequest();
    let url = '/api/asks'
    http.onreadystatechange = () => {
        if(http.readyState === http.DONE){
            asks = http.response;
            asksCnt = Object.keys(asks).length;
            index = 0;

            set_elementAsks();
        }
    };

    http.open('GET', url, true);
    http.responseType = 'json';
    http.send();
}

function set_elementAsks(){
    for(let i = 0; i < 10 && index < asksCnt; i++, index++){
        let li = document.createElement('li');
        li.className = 'ask';

        if(user == 'admin'){
            let span = document.createElement('span');

            let button = document.createElement('a');
            button.setAttribute('href', '#');
            button.setAttribute('onclick', 'delete_ask("' + asks[index].url + '")');

            let img = document.createElement('img');
            img.setAttribute('src', '/static/image/delete.png');
            
            button.append(img);
            span.appendChild(button);
        }

        let name = document.createElement('span');
        name.append(asks[index].name);
        name.append('(url : ' + asks[index].url + ')');
        li.appendChild(name);

        elementAsks.appendChild(li);
    }
}

function delete_ask(url){
    let http = new XMLHttpRequest();
    let url = '/api/asks';
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

    http.open('DELETE', url, true);
    http.responseType = 'json';
    http.setRequestHeader('Content-type', 'application/json');
    http.send(JSON.stringify({'url' : url}));
}

function get_prev_list(){
    if(index - 10 < 0){
        set_msg('First page', 1);
        return;
    }
    else{
        index -= 10;
        set_elementAsks();
    }
}

function get_next_list(){
    if(index >= asksCnt){
        set_msg('Last page', 1);
        return;
    }
    else{
        set_elementAsks();
    }
}