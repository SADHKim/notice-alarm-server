var check_id = false;

window.onload = function () {
    let id = document.getElementById('user_id');

    id.onchange = function(){
        check_id = false;
        document.getElementById('id_comment').style.display = 'none';
    };
}

function check_overlap(){
    if(!document.register_form.id.value){
        alert('input ID first', 0);
        return;
    }

    let http = new XMLHttpRequest();
    let url = '/api/id_overlap';
    http.onreadystatechange = () => {
        if (http.readyState === http.DONE) {
            let response = http.response;
            
            if(response.error == 0){
                check_id = true;
        
                let element = document.getElementById('id_comment');
                element.textContent = response.msg;
                element.style.color = "green";
                element.style.display = 'block';
            }
            else{
                let element = document.getElementById('id_comment');
                element.textContent = response.msg;
                element.style.color = "red";
                element.style.display = 'block';
            }
        }
    };

    http.open('POST', url, true);
    http.responseType = 'json'
    http.setRequestHeader("Content-Type", "application/json");

    http.send(JSON.stringify({'id' : document.register_form.id.value}));
}

function register_check(){
    if(!document.register_form.id.value){
        alert('input ID', 1);
        document.register_form.id.focus();
        return false;
    }
    if(!document.register_form.passwd.value){
        alert('input PASSWORD', 1);
        document.register_form.passwd.focus();
        return false;
    }
    if(document.register_form.passwd.value != document.register_form.passwd_1.value){
        alert('no match password', 1);
        document.register_form.passwd.select();
        return false;
    }
    if(!document.register_form.email.value){
        alert('input EMAIL', 1);
        document.register_form.email.focus();
        return false;
    }
    
    if(check_id) return true;
    else{
        alert('check your ID can usable', 1);
        return false;
    }
}

