### 소프트웨어 마에스트로 홈페이지 공지사항 크롤링 ###

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

prev_posts = []
flag = False
    
def searchUpdate(driver, url):
    global prev_posts
    global flag
    
    ret = []
    tmp = []
    
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.gallaylist')))
    
    posts = driver.find_element(By.CSS_SELECTOR, '.gallaylist').find_elements(By.TAG_NAME, 'h3')
    
    
    for post in posts:
        title = post.get_attribute('innerText').strip()
        
        if not title in prev_posts and flag:
            ret.append(title)
        
        tmp.append(title)
        
    if not flag:
        flag = True
        
    prev_posts = tmp
    
    return ret
    
    
    
def sw_maestro_crawling(driver):
    url = 'https://www.swmaestro.org/sw/bbs/B0000003/list.do?menuNo=200020'
    
    ret_value = searchUpdate(driver, url)
    if len(ret_value) >= 1:
        return ('sw_maestro', url, ret_value)
    else:
        return False