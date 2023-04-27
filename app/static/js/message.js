function set_msg(msg, error){
    let container = document.getElementById('message');
    let img = document.getElementById('msgImg');
    let content = document.getElementById('msgContent');

    container.style.display = 'none';
    content.innerText = msg;
    if (error == 1)
        img.setAttribute('src', '/static/image/wrong.png');
    else
        img.setAttribute('src', '/static/image/checked.png');
    container.style.display = 'block';
}



function api_check_id_overlap(id){
    

    while(res == undefined){};
    return res;
}