from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conf import name2path, prev_lists

# 크롬 드라이버 경로
chromedriver_path = '/usr/bin/chromedriver'

# 웹 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')  # 브라우저 백그라운드 실행
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

    
def get_posts(website, url):
    
    ret = [] # 리턴하는 값 : 새로 추가된 게시글 #
    tmp = [] # 새로 크롤링한 게시글들을 저장하는 리스트 #
    
    path = name2path[website]
    
    
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, path['class'])))
    
    posts = driver.find_element(By.CSS_SELECTOR, path['class']).find_elements(By.TAG_NAME, path['tag'])
    
    flag = False
    if len(prev_lists[website]) >= 1:
        flag = True
    
    for post in posts:
        title = post.get_attribute('innerText').strip()
        
        if not title in prev_lists[website] and flag:
            ret.append(title)
        
        tmp.append(title)
        
    prev_lists[website] = tmp
    
    return ret
    

def crawling(site):
    
    posts = get_posts(site['name'], site['url'])
    
    if len(posts) >= 1:
        return (site['name'], site['url'], posts)
    else:
        return False