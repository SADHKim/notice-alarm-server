from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import time

posts_list = []

# 크롬 드라이버 경로
chromedriver_path = '/Users/seongah/Documents/chromedriver_mac64/chromdriver'

# 웹 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')  # 브라우저 백그라운드 실행
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

def searchUpdate(url):
    # 페이지 열기
    driver.get(url)

    # 페이지가 로드될 때까지 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.bbs_con')))

    # 게시글 목록 추출
    table = driver.find_element(By.CSS_SELECTOR, '.bbs_con')
    rows = table.find_elements(By.TAG_NAME, 'tr')[1:]

    posts_element = driver.find_element(By.CSS_SELECTOR, '.bbs_con').find_elements(By.TAG_NAME, 'tr')[1:]
    for i in range(len(posts_element)):
        posts_title = posts_element[i].find_elements(By.TAG_NAME, "a")[0].get_attribute("text").strip()
        if not posts_title in posts_list:
            posts_list.append(posts_title)
            print(posts_title)

def hyu_cs_board_crawling():
    # 크롤링할 페이지의 URL
    url = 'http://cs.hanyang.ac.kr/board/gradu_board.php'
    schedule.every(1).minutes.do(lambda: searchUpdate(url))

    while 1:
        schedule.run_pending()
        time.sleep(1)

        
if __name__ == "__main__":
	hyu_cs_board_crawling()