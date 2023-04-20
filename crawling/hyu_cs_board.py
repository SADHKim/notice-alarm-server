from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


posts_list = []
isStarted = False
def searchUpdate(driver, url):
    global posts_list
    global isStarted
    
    ret = []
    
    
    # 페이지 열기
    driver.get(url)

    # 페이지가 로드될 때까지 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.bbs_con')))

    # 게시글 목록 추출
    table = driver.find_element(By.CSS_SELECTOR, '.bbs_con')
    rows = table.find_elements(By.TAG_NAME, 'tr')[1:]

    posts_element = driver.find_element(By.CSS_SELECTOR, '.bbs_con').find_elements(By.TAG_NAME, 'tr')[1:]
    
    idx = 0
    for post in posts_element:
        post_title = post.find_elements(By.TAG_NAME, "a")[0].get_attribute("text").strip()
        
        if not post_title in posts_list and isStarted:
            ret.append(post_title)
            tmp_posts.insert(idx, post_title)
            dix += 1
        elif not isStarted:
            posts_list.append(post_title)
    
                              
    if not isStarted:
        isStarted = True
        
    if len(posts_element) < len(posts_list):
        tmp = len(posts_list) - len(posts_element)
        for i in range(tmp):
            posts_list.pop()
    
            
    return ret
    

def hyu_cs_board_crawling(driver):
    # 크롤링할 페이지의 URL
    url = 'http://cs.hanyang.ac.kr/board/gradu_board.php'

    posts = searchUpdate(driver, url)
    if len(posts) >= 1:
        return ('hyu_cs_board', url, posts)
    else:
        return False
