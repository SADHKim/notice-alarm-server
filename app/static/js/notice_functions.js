var currNotice;

function close_view(){
    document.getElementById('notice-view').style.display = 'none';
}
function open_view(num){
    let http = new XMLHttpRequest();
    let url = '/api/notices?num=' + num;
    http.onreadystatechange = () =>{
        if(http.readyState === http.DONE){

            currNotice = num;
            
            document.getElementById('notice-title').innerText = http.response.title;
            document.getElementById('notice-time').innerText = http.response.time;
            document.getElementById('notice-content').innerText = http.response.content;
            
            document.getElementById('notice-view').style.display = 'block';
        }
    };
    http.responseType = 'json';
    http.open('GET', url, true);
    http.send();
}

function delete_notice(){
    let http = new XMLHttpRequest();
    let url = '/notice'
    http.onreadystatechange = () =>{
        if(http.readyState === http.DONE){
            if(http.response.error == 0){
                location.reload(true);
            }
            else if(http.response.error == -1){
                alert(http.response.msg);
            }
        }
    }

    http.open('DELETE', url, true);
    http.setRequestHeader('Content-type', 'application/json');
    http.responseType = 'json';
    http.send(JSON.stringify({'num' : currNotice}));
}