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