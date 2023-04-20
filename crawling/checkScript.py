from selenium import webdriver

from .hyu_cs_board import hyu_cs_board_crawling


# 웹 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')  # 브라우저 백그라운드 실행
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)



def check_script():
    result = []
    
    result.append(hyu_cs_board_crawling(driver))
    
    return result