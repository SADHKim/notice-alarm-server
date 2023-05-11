### sending mail to users.
### this file get users' mail address from getMailList.py with name of websites

import smtplib
from email.mime.text import MIMEText
from conf import MAIL_ID, MAIL_PWD

### the function sends mail with class object, recievers as params ###
### classObj has mail subject, content, and link ###
def send_mail(classObj, recievers):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()

    smtpObj.login(MAIL_ID, MAIL_PWD)
    
    mailContent = '<p>' + classObj.content + '</p>'
    mailContent += '<a href="' + classObj.link + '">' + classObj.link + '</a>'
        
    msg = MIMEText(mailContent, 'html')
    msg['Subject'] = classObj.subject
    
    ### recievers, second parameter, can send more than one if recievers is the list of string ###
    smtpObj.sendmail(MAIL_ID, recievers, msg.as_string())

def send_start_mail(sites):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    
    smtpObj.login(MAIL_ID, MAIL_PWD)
    
    mailContent = '''<p>
    총 %s개의 사이트에서 크롤링을 시작합니다
    </p>''' % str(len(sites))
    
    msg = MIMEText(mailContent, 'html')
    msg['Subject'] = '[notice-alarm] Selenium 크롤링을 시작합니다'
    
    smtpObj.sendmail(MAIL_ID, ['kdh101800@gmail.com', 'kimsa0322@gmail.com'], msg.as_string())
    
    
def send_error_mail(site):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    
    smtpObj.login(MAIL_ID, MAIL_PWD)
    
    mailContent = '''<p>
    사이트 [%s] 크롤링 중에 오류가 발생했습니다.<br>
    <br>
    url : <a href="%s" target="_blank">%s</a><br>
    className : %s<br>
    path : %s<br>
    </p>''' % (site['name'], site['url'], site['url'], site['class'], site['path'])
    
    msg = MIMEText(mailContent, 'html')
    msg['Subject'] = '[notice-alarm] 크롤링 중에 오류가 발생했습니다'
    
    smtpObj.sendmail(MAIL_ID, ['kdh101800@gmail.com', 'kimsa0322@gmail.com'], msg.as_string())