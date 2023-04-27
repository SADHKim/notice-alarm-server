var siteIndex;
var elementWebList;
var websites;
var websitesCnt;
var user;

window.onload = function (){
    elementWebList = document.getElementById('user_websites');
    set_websites();
};

function set_websites(){
    let http = new XMLHttpRequest();
    let url = '/api/websites?user=' + user;
    http.onreadystatechange = () => {
        if (http.readyState === http.DONE) {
            websites = http.response;
            siteIndex = 0;
            websitesCnt = Object.keys(websites).length;
            set_elementWebList();
        }
    };
    http.open('GET', url, true);
    http.responseType = 'json';
    http.setRequestHeader("Content-Type", "application/json");

    http.send();
}

function set_user(userID){
    user = userID;
}

function set_elementWebList (){
    elementWebList.innerHTML = '';

    let title = document.createElement('li');
    let strong = document.createElement('h1');
    strong.append('알림받는 웹사이트');
    title.appendChild(strong);
    elementWebList.appendChild(title);

    for(let i = 0; i < 10 && siteIndex < websitesCnt; siteIndex++, i++){
        let li = document.createElement('li');
        li.className = 'website';
        
        let a = document.createElement('a');
        a.setAttribute('href', '#');
        a.setAttribute('onclick', 'deleteWeb("' + websites[siteIndex].website_name + '")');

        let spanImg = document.createElement('span');
        let img = document.createElement('img');
        img.setAttribute('src', '/static/image/delete.png');
        spanImg.append(img);

        a.append(spanImg)
        li.appendChild(a);

        let spanTitle = document.createElement('span');
        spanTitle.append(websites[siteIndex].website_name);
        li.append(spanTitle)

        elementWebList.appendChild(li);
    }
}

function deleteWeb(website){
    let result = confirm(website + '을(를) 삭제하고, 더 이상 알람을 받지 않겠습니까?');
    if(result){
        let http = new XMLHttpRequest();
        let url = '/api/websites';
        http.onreadystatechange = () => {
            if (http.readyState === http.DONE) {
                let response = http.response;
                if(response.error == 0){
                    set_msg(response.msg, response.error);
                    set_websites();
                }
                else{
                    set_msg(response.msg, response.error);
                }
            }
        };

        http.open('DELETE', url, true);
        http.responseType = 'json';
        http.setRequestHeader('Content-type', 'application/json');
        http.send(JSON.stringify({'user' : user, 'website' : website}));
    }
    else{
        return;
    }
}

function change_password(){
    if(!document.change_pass_form.currPass.value){
        set_msg('Input current password', 1);
        return;
    }
    if(!document.change_pass_form.newPass.value){
        set_msg('Input new password', 1);
        return;
    }

    let http = new XMLHttpRequest();
    let url = '/api/change/password';
    http.onreadystatechange = () => {
        if (http.readyState === http.DONE) {
            let response = http.response;

            if(response.error == 0){
                set_msg(response.msg, response.error);
            }
            else{
                set_msg(response.msg, response.error);
            }
        }
    };

    http.responseType = 'json';
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/json');
    http.send(JSON.stringify({'user' : user, 'currPass' : document.change_pass_form.currPass.value, 'newPass' : document.change_pass_form.newPass.value}));
}

function change_email(){
    if(!document.change_email_form.newEmail.value){
        set_msg('Input new email', 1);
        return;
    }

    let http = new XMLHttpRequest();
    let url = '/api/change/email';
    http.onreadystatechange = () => {
        if (http.readyState === http.DONE) {
            let response = http.response;
            
            if (response.error == 0){
                set_msg(response.msg, response.error);
                update_email();
            }
            else{
                set_msg(response.msg, response.error);
            }
        }
    };

    http.responseType = 'json';
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/json');
    http.send(JSON.stringify({'user' : user, 'newEmail' : document.change_email_form.newEmail.value}));
}

function update_email(){
    let http = new XMLHttpRequest();
    let url = '/profile?user=' + user;
    http.onreadystatechange = () => {
        if (http.readyState === http.DONE) {
            let response = http.response;
            let currEmail = document.getElementById('currEmail');
            currEmail.innerText = response.email;
        }
    };

    http.responseType = 'json';
    http.open('GET', url, true);
    http.send();
}

function get_prev_list(){
    if(siteIndex  - 10 < 0){
        alert('first page');
        return;
    }
    else{
        siteIndex -= 10;
        set_elementWebList();
    }
}

function get_next_list(){
    if(siteIndex >= websitesCnt){
        alert('last page');
        return;
    }
    else{
        set_elementWebList();
    }
}