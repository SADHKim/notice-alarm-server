var elementAsks;
var asksCnt;
var asks;
var index;


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
    elementAsks.innerHTML = '';

    if(asksCnt == 0){
        let li = document.createElement('li');
        li.append('There are no asks.');
        elementAsks.appendChild(li);
        return;
    }

    for(let i = 0; i < 10 && index < asksCnt; i++, index++){
        let li = document.createElement('li');
        li.className = 'ask';

        if(typeof(append_delete) == 'function') li = append_delete(li);

        let name = document.createElement('span');
        name.append(asks[index].name);
        name.append('(url : ' + asks[index].url + ')');
        li.append(name);

        elementAsks.appendChild(li);
    }
}

function search(){
    let keyword = document.search.value;
    let http = new XMLHttpRequest();
    let url = '/api/asks?keyword=' + keyword;
    http.onreadystatechange = () => {
        if(http.readyState === http.DONE){
            asks = http.response;
            index = 0;
            asksCnt = Object.keys(asks).length;

            set_elementAsks();
        }
    }
    http.responseType = 'json'
    http.open('GET', url, true)
    http.send()
}

function get_prev_list(){
    if(index <= 10){
        set_msg('First page', 1);
        return;
    }
    else{
        index = index - 10 - (index % 10);
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