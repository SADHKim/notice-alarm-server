### sending mail to users.
### this file get users' mail address from getMailList.py with name of websites

import smtplib
from email.mime.text import MIMEText

### the function sends mail with class object, recievers as params ###
### classObj has mail subject, content, and link ###
def send_mail(classObj, recievers, mailId, mailPwd):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()

    smtpObj.login(mailId, mailPwd)
    
    mailContent = '<p>' + classObj.content + '</p>'
    if classObj.link != "":
        '<a href="' + classObj.link + '">' + classObj.link + '</a>'
        
    msg = MIMEText(mailContent, 'html')
    msg['Subject'] = classObj.subject
    
    ### recievers, second parameter, can send more than one if recievers is the list of string ###
    smtpObj.sendmail('kdh101800@gmail.com', recievers, msg.as_string())