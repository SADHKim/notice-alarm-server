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
    let comment = document.getElementById('find-form-comment')
    comment.innerHTML = '<div class="d-flex justify-content-center">\
        <div class="spinner-border text-primary" role="status">\
            <span class="sr-only">Loading...</span>\
        </div>\
    </div>'
    comment.style.display = 'block'

    let id = document.getElementById('find-form-id').value;
    let email = document.getElementById('find-form-email').value;

    let http = new XMLHttpRequest();
    let url = '/api/find-password';

    http.onreadystatechange = () =>{
        if(http.readyState == http.DONE){
            if(http.response.error == 0){
                let body = document.getElementById('modal-body');
                body.innerHTML = '비밀번호가 재설정되었습니다.<br>';
                body.innerHTML += '등록된 E-mail을 통해 변경된 비밀번호를 안내해드립니다.<br>';
                body.innerHTML += '로그인 후에 비밀번호를 변경하세요.';

                document.getElementById('find-form-submit').style.display = 'none';
            }
            else if(http.response.error == 1){
                let comment = document.getElementById('find-form-comment')
                comment.innerText = '입력하신 ID 혹은 Email이 올바르지 않습니다. 다시 시도해주세요.';
                comment.style.display = 'block'
            }
            else{
                let comment = document.getElementById('find-form-comment')
                comment.innerText = '오류가 발생했습니다. 나중에 다시 시도해주세요.';
                comment.style.display = 'block'
            }
        }
    }

    http.open('post', url, true);
    http.responseType = 'json';
    http.setRequestHeader('Content-type', 'application/json');

    http.send(JSON.stringify({'id' : id, 'email' : email}));
}

function close_modal(){
    let body = document.getElementById('modal-body')
    body.innerHTML = '사용자의 아이디와 등록한 이메일 주소를 입력해주세요.<br>\
    임의로 비밀번호를 설정해서 등록된 Email을 통해 알려드립니다.<br><br>\
    \
    <form>\
        <div class="form-group">\
            <label for="find-from-id">Your ID</label>\
            <input type="text" class="form-control" id="find-form-id" placeholder="ID" required>\
        </div>\
        <div class="form-group">\
            <label for="find-form-email">Email Address</label>\
            <input type="email" class="form-control" id="find-form-email" placeholder="Email" required>\
        </div>\
    </form>\
    \
    <div class="text-danger small" style="display: none;" id="find-form-comment"></div>';

    document.getElementById('find-form-comment').style.display = 'none';
}