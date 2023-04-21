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
    smtpObj.sendmail('kdh101800@gmail.com', recievers, msg.as_string())