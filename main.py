import inform
import crawling
import config

mailId = config.MAIL_ID
mailPwd = config.MAIL_PWD

dbName = config.DB_NAME
dbId = config.DB_ID
dbPwd = config.DB_PWD

def main():
    link = crawling.hyu_cs_board_crawling()
    
    if link != False:
        noticeObj = inform.Notice()
        noticeObj.make_script('content for combine', '')
        noticeObj.make_title('the title', 'somewebsite')
        
        recievers = ['kdh101800@gmail.com', 'ken1934@naver.com']
        
        inform.send_mail(noticeObj, recievers, mailId, mailPwd)
        

if __name__ == '__main__':
    main()