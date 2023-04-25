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

    return true;
}

