function login_check(){
    if(!document.login_form.id){
        set_msg('input ID', 1);
        document.login_form.id.focus();
        return false;
    }
    if(!document.login_form.passwd){
        set_msg('input PASSWORD', 1);
        document.login_form.passwd.focus();
        return false;
    }

    return true;
}