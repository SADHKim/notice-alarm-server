var siteIndex = 0;
var elementWebList;
var websites;
var websitesCnt;
var user;

window.onload = function (){
    elementWebList = document.getElementById('user_websites');

    let http = new XMLHttpRequest();
    url = '/api/websites?user=' + user;
    http.onreadystatechange = function(){
        if (http.readyState === http.DONE){
            websites = http.response;
            websitesCnt = Object.keys(websites).length;

            set_elementWebList();
        }
    };
    http.open('GET', url, true);
    http.responseType = 'json';
    http.send();
};

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
        a.setAttribute('onclick', 'deleteWeb("' + user + '", "' +  websites[siteIndex].website_name + '")');

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

function get_prev_list(){
    siteIndex -= 10;
    if(siteIndex < 0){
        alert('first page');
        return;
    }
    else{
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

function deleteWeb(user, website){
    let result = confirm(website + '을(를) 삭제하고, 더 이상 알람을 받지 않겠습니까?');
    if(result){
        url = '/profile/delete?user=' + user + '&website=' + website;
        location.href = url
    }
    else{
        return;
    }
}