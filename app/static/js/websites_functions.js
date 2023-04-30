var elementWebsites;
var websites;
var index = 0;
var websitesCnt;
var user = 'guest';

window.onload = function(){
    elementWebsites = document.getElementById('websites');
    set_websites()
};

function set_user(userId){user = userId;}

function set_websites(){
    let http = new XMLHttpRequest();
    let url = '/api/websites';

    http.onreadystatechange = () =>{
        if(http.readyState === http.DONE){
            index = 0;
            websites = http.response;
            websitesCnt = Object.keys(websites).length;
            
            set_elementWebsites();
        }
    };
    http.open('GET', url, true);
    http.responseType = 'json';
    http.send();
}

function set_elementWebsites(){
    elementWebsites.innerHTML = '';

    for(let i = 0; i < 10 && index < websitesCnt; i++, index++){
        let li = document.createElement('li');
        li.className = 'website';

        if (typeof(append_delete) == 'function') {li = append_delete(li);}
        else{
            let mark = document.createElement('span');

            let a = document.createElement('a');
            a.setAttribute('href', '#');
            a.setAttribute('onclick', 'add_website("' + user + '", "' + websites[index].name + '")');

            let img = document.createElement('img');
            img.setAttribute('src', '/static/image/add.svg');

            a.append(img);
            mark.append(a);
            li.appendChild(mark);
        }

        let name = document.createElement('span');
        name.append(websites[index].name + ' (url : ' + websites[index].url + ')');

        li.appendChild(name);
        elementWebsites.appendChild(li);
    }
}

function get_prev_list(){
    if(index <= 10){
        set_msg('First page', 1);
        return;
    }
    else{
        index = index - 10 - (index % 10);
        set_elementWebsites();
    }
}

function get_next_list(){
    if(index >= websitesCnt){
        set_msg('Last page', 1);
        return;
    }
    else{
        set_elementWebsites();
    }
}

function add_website(id, website){
    if(id == 'guest'){
        set_msg('Login first', 1);
        return;
    }
    
    const add = (user, email, website) => {
        let http = new XMLHttpRequest();
        let url = '/api/websites'
        http.onreadystatechange = () => {
            if(http.readyState === http.DONE){
                let response = http.response;

                if (response.error == 0){
                    set_msg(response.msg, response.error);
                }
                else{
                    set_msg(response.msg, response.error);
                }
            }
        };

        http.open('POST', url, true);
        http.setRequestHeader('Content-type', 'application/json');
        http.responseType = 'json';
        http.send(JSON.stringify({'user' : user, 'email' : email, 'website' : website}));
    };

    let http = new XMLHttpRequest();
    let url = '/profile?user=' + id;
    http.onreadystatechange = () => {
        if(http.readyState === http.DONE){
            let response = http.response;
            add(response.id, response.email, website);
        }
    }

    http.open('GET', url, true);
    http.responseType = 'json';
    http.send();
}