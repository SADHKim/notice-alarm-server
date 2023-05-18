function login_check(){
    if(!document.login_form.id){
        alert('input ID', 1);
        document.login_form.id.focus();
        return false;
    }
    if(!document.login_form.passwd){
        alert('input PASSWORD', 1);
        document.login_form.passwd.focus();
        return false;
    }

    return true;
}

function find_password(){
    let id = document.find_form.id.value;
    let email = document.find_form.email.value;

    let http = new XMLHttpRequest();
    let url = '/api/find-password';

    http.onreadystatechange = () =>{
        if(http.readyState == http.DONE){
            if(http.response.error == 0){
                let body = document.getElementById('modal-body');
                let pass = http.response.pass;
                body.innerHTML = '비밀번호가 재설정되었습니다.<br>';
                body.innerHTML += '비밀번호는 <span class="text-primary">' + pass + '</span>입니다.<br>';
                body.innerHTML += '로그인 후에 비밀번호를 변경하세요.';

                document.getElementById('find-form-submit').style.display = 'none';
            }
            else if(http.response.error == 1){
                let body = document.getElementById('modal-body');
                
                let script = document.createElement('p');
                script.className = 'text-danger small';
                script.innerText = '입력하신 ID 혹은 Email이 올바르지 않습니다. 다시 시도해주세요';
            }
            else{
                let body = document.getElementById('modal-body');
                
                let script = document.createElement('p');
                script.className = 'text-danger small';
                script.innerText = '오류가 발생했습니다. 나중에 다시 시도해주세요.';   
            }
        }
    }

    http.open('post', url, true);
    http.responseType = 'json';
    http.setRequestHeader('Content-type', 'application/json');

    http.send(JSON.stringify({'id' : id, 'email' : email}));
}