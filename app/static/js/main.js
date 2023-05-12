var lang_intro = 'korean'
var lang_tuto = 'korean'

function interpre_intro() {
    let intro = document.getElementById('intro')
    let intro_btn = document.getElementById('intro-btn')
    let tutorial = document.getElementById('go2Tutorial')

    

    if (lang_intro == 'korean'){
    let script = "Hello, we launched the service under the name of Notice Alarm! <br>";
    script += "Our service started with the idea of <strong>providing more convenient</strong> announcements to users.. <br><br>";
    script += "When you register a site where you want to receive notifications, we will notify you of new announcements through your <span class=\"text-primary\">email!</span> <br><br>";
    script += "Please refer to the tutorial below for how to use the service!<br><br>";
    script += "Error Contact : <span class=\"text-primary\">notice.alarm.hanyang@gmail.com</span>"

    intro.innerHTML = script;
    intro_btn.innerText = '한국어';
    tutorial.innerHTML = "Tutorial<i class=\"bi bi-link-45deg\"></i>"
    lang_intro = 'english'
    }
    else if(lang_intro == 'english'){
        let script = "Notice Alarm이라는 이름으로 서비스를 출시했습니다! <br>"
        script += "우리 서비스는 사용자에게 궁금한 공지사항을 조금이라도 <strong>편리하게 제공하고 싶은</strong> 생각에서 출발했습니다.. <br><br>"
        script += "알림을 받고 싶은 사이트를 등록하면, 사용자의 <span class=\"text-primary\">E-mail</span>을 통해 새로운 공지사항을 알려드립니다! <br><br>"
        script += "서비스 이용방법은 다음을 참고해주세요! <br><br>"
        script += "버그 문의 : <span class=\"text-primary\">notice.alarm.hanyang@gmail.com</span>"

        intro.innerHTML = script;
        intro_btn.innerText = 'English';
        tutorial.innerHTML = "서비스 이용방법 보러가기<i class=\"bi bi-link-45deg\"></i>"
        lang_intro = 'korean'
    }
}

function interpre_tuto(){
    let btn = document.getElementById('tutorial-btn')
    let title = document.getElementById('tutorial-title')
    let script = document.getElementById('tutorial-script')
    let profile = document.getElementById('tutorial-profile')
    let websites = document.getElementById('tutorial-websites')
    let ask = document.getElementById('tutorial-ask')
    let notice = document.getElementById('tutorial-notice')

    if(lang_tuto == 'korean'){
        let content = 'Tutorial'
        title.innerText = content

        content = 'Our service can be divided <span style="color: rgb(62, 133, 75);">four section</span>.<br>';
        content += '<ul><li style="color: rgb(27, 161, 143);">Profile</li><li style="color: rgb(27, 161, 143);">Websites</li><li style="color: rgb(27, 161, 143);">Ask</li><li style="color: rgb(27, 161, 143);">Notice</li></ul>'
        content += 'For a description of each section, open the card below'
        script.innerHTML = content

        content = 'This page shows user information<br>'
        content += 'You can change password, e-mail<br>and manage your website list<br><br>'
        content += '<a href="/profile" class="text-primary">go to Profile<i class="bi bi-link-45deg"></i></a>'
        profile.innerHTML = content

        content = 'This page shows website list that is provided<br>'
        content += 'You can add websites where you want to know notices<br>'
        content += 'and recieve alarm through e-mail<br><br>'
        content += '<a href="/websites" class="text-primary">go to Websites<i class="bi bi-link-45deg"></i></a>'
        websites.innerHTML = content

        content = 'Users can ask new websites on this page<br>'
        content += 'If you ask new website not provided in Websites page,<br>'
        content += 'administrator will check and add the website<br><br>'
        content += 'before you ask website, check url if the url is exists on Ask page!<br><br>'
        content += '<a href="/websites/ask" class="text-primary">go to Ask<i class="bi bi-link-45deg"></i></a>'
        ask.innerHTML = content

        content = 'This page shows notices of our service<br>'
        content += 'We will post notices about adding websites, answer of asks, and etc<br><br>'
        content += 'You can recieve alarm our notices also<br><br>'
        content += '<a href="/notice" class="text-primary">go to Notice<i class="bi bi-link-45deg"></i></a>'
        notice.innerHTML = content

        btn.innerText = '한국어'
        lang_tuto = 'english'
    }
    else if(lang_tuto == 'english'){
        let content = '서비스 이용방법'
        title.innerText = content;

        content = '우리 서비스는 총 <span style="color: rgb(62, 133, 75);">4가지 섹션</span>으로 구분할 수 있습니다. <br>'
        content += '<ul><li style="color: rgb(27, 161, 143);">Profile</li><li style="color: rgb(27, 161, 143);">Websites</li><li style="color: rgb(27, 161, 143);">Ask</li><li style="color: rgb(27, 161, 143);">Notice</li></ul>'
        content += '각각의 섹션에 대한 설명은 아래 카드를 열어보세요'
        script.innerHTML = content

        content = '유저 정보를 보여주는 페이지입니다<br>'
        content += '비밀번호 변경, 알림받는 E-mail 변경 기능이 있으며<br>'
        content += '알림받는 사이트를 확인하고 관리할 수 있습니다<br><br>'
        content += '<a href="/profile" class="text-primary">Profile 바로가기<i class="bi bi-link-45deg"></i></a>'
        profile.innerHTML = content

        content = '우리 서비스에서 제공하는 웹사이트를 보여주는 페이지입니다<br>'
        content += 'Websites 페이지에서 공지사항을 알고 싶은 사이트를 추가하고<br>'
        content += 'E-mail을 통해 알림을 받을 수 있습니다<br><br>'
        content += '<a href="/websites" class="text-primary">Websites 바로가기<i class="bi bi-link-45deg"></i></a>'
        websites.innerHTML = content

        content = '사용자들이 새로운 웹사이트를 요청하는 페이지입니다<br>'
        content += 'Websites 페이지에서 제공하지 않는 사이트를 해당 페이지에 요청하면<br>'
        content += '관리자가 확인 후 Websites 페이지에 추가합니다<br><br>'
        content += '웹사이트를 요청하기 전에, Ask 페이지에 본인이 요청할 페이지의 url이 존재하는지 먼저 확인하세요! <br><br>'
        content += '<a href="/websites/ask" class="text-primary">Ask 바로가기<i class="bi bi-link-45deg"></i></a>'
        ask.innerHTML = content

        content = 'Notice Alarm의 공지 페이지입니다<br>'
        content += '해당 페이지에서 우리 서비스의 공지사항을 제공합니다<br><br>'
        content += 'Websties 추가, Ask 답변 등을 게시할 예정입니다<br>'
        content += '우리 서비스의 공지사항도 알림으로 받아볼 수 있습니다<br><br>'
        content += '<a href="/notice" class="text-primary">Notice 바로가기<i class="bi bi-link-45deg"></i></a>'
        notice.innerHTML = content

        btn.innerText = 'English'
        lang_tuto = 'korean'
    }
}