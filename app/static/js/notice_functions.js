var elementNotices;
var notices;
var noticesCnt;
var index;
var currNotice = -1;

function close_view(){
    document.getElementById('view').style.display = 'none';
}
function open_view(num){
    let http = new XMLHttpRequest();
    let url = '/api/notices?num=' + num;
    http.onreadystatechange = () =>{
        if(http.readyState === http.DONE){
            currNotice = num;
            
            document.getElementById('notice_title').innerText = http.response.title;
            document.getElementById('notice_date').innerText = http.response.time;
            document.getElementById('notice_content').innerText = http.response.content;
            
            document.getElementById('view').style.display = 'block';
        }
    };
    http.responseType = 'json';
    http.open('GET', url, true);
    http.send();
}

window.onload = () => {
    elementNotices = document.getElementById('notices');
    set_notices();
};

function set_notices(){
    let http = new XMLHttpRequest();
    let url = '/api/notices';
    http.onreadystatechange = () =>{
        if(http.readyState === http.DONE){
            notices = http.response;
            index = 0;
            noticesCnt = Object.keys(notices).length;
            set_elementNotices();
        }
    };
    http.responseType = 'json';
    http.open('GET', url, true);
    http.send();
}

function set_elementNotices(){
    elementNotices.innerHTML = '';

    if(noticesCnt == 0){
        set_msg('There are no notices...', 1);
        return;
    }

    for(let i = 0; i < 10 && index < noticesCnt; i++, index++){
        let tr = document.createElement('tr');

        let num = document.createElement('td');
        num.append(noticesCnt - index);

        let title = document.createElement('td');
        title.className = 'notice';
        let a = document.createElement('a');
        a.setAttribute('href', '#');
        a.setAttribute('onclick', 'open_view("' + notices[index].num + '")');
        a.append(notices[index].title);
        title.append(a);

        let writer = document.createElement('td');
        writer.append(notices[index].writer);

        let time = document.createElement('td');
        time.append(notices[index].time);

        tr.appendChild(num);
        tr.appendChild(title);
        tr.appendChild(writer);
        tr.appendChild(time);

        elementNotices.appendChild(tr);
    }
}

function get_prev_list(){
    if(index <= 10){
        set_msg('First page', 1);
        return;
    }
    else{
        index = index - 10 - (index % 10);
        set_elementNotices();
    }
}
function get_next_list(){
    if(index >= noticesCnt){
        set_msg('Last page', 1);
        return;
    }
    else{
        set_elementNotices();
    }
}