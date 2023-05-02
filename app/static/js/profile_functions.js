function delete_user_website(user, website){
    let result = confirm(website + ' 을(를) 삭제하고, 더 이상 알람을 받지 않겠습니까?');
    if(result){
        let http = new XMLHttpRequest();
        let url = '/api/websites';
        http.onreadystatechange = () => {
            if (http.readyState === http.DONE) {
                let response = http.response;
                if(response.error == 0){
                    location.reload(true);
                }
                else{
                    alert('error')
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