var check_id = false;

window.onload = function () {
    let id = document.getElementById('user_id');

    id.onchange = function(){
        check_id = false;
        document.getElementById('id_comment').textContent = "";
    };
}

function id_overlap(){
    let url = '/api/id_overlap_check';

    let http = new XMLHttpRequest();
    http.onreadystatechange = function(){
        if(http.readyState === http.DONE){
            let response = http.response;

            if(response.msg == 'ok'){
                check_id = true;

                let element = document.getElementById('id_comment');
                element.textContent = "the ID can be used";
                element.style.color = "green";
            }
            else{
                let element = document.getElementById('id_comment');
                element.textContent = "the ID can't be used";
                element.style.color = "red";
            }
        }
    };

    http.open("POST", url, true);
    http.responseType = 'json';
    http.setRequestHeader("Content-Type", "application/json");
    http.send(JSON.stringify({'id' : document.register_form.id.value}));
}

function register_check(){
    if(!document.register_form.id.value){
        alert('input id');
        document.register_form.id.focus();
        return false;
    }
    if(!document.register_form.passwd.value){
        alert('input password');
        document.register_form.passwd.focus();
        return false;
    }
    if(document.register_form.passwd.value != document.register_form.passwd_1.value){
        alert('no mat password');
        document.register_form.passwd.slelct();
        return false;
    }
    if(!document.register_form.email.value){
        alert('input email');
        document.register_form.email.focus();
        return false;
    }
    
    if(check_id) return true;
    else{
        alert('중복확인을 진행하세요');
        return false;
    }
}

