function login_check(){
    if(!document.login_form.id){
        alert('input id');
        document.login_form.id.focus();
        return false;
    }
    if(!document.login_form.passwd){
        alert('input password');
        document.login_form.passwd.focus();
        return false;
    }

    return true;
}