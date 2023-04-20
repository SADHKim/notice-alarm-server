import inform
import crawling


def main():
    # 크롤링의 결과값 저장 (False or websitename, url, posts : list) #
    checkResult = crawling.check_script()
    
    for result in checkResult:
        if result is False:
            continue
        
        # Notice object 생성, 내용 만들기 #
        script = inform.Notice()
        script.make_script(result[2], result[1])
        script.make_title(result[2], result[0])
        
        # 해당 웹사이트에서 알림을 받는 사람들 추출#
        recievers = inform.get_recievers(result[0])
        # 메일 전송 #
        inform.send_mail(script, recievers)
        
        
if __name__ == '__main__':
    main()