from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 서울%20브롬톤
search = input('검색단어 => ')
driver = webdriver.Chrome()  # 크롬웹브라우저를 생성
driver.get(f'https://www.daangn.com/search/{search}/') # 로그인하기 위한 사이트주소
time.sleep(1)   # 3초지연(대기시간)

loop = True
i = 0
while loop:
    i += 1
    try:
        more_btn = driver.find_element(By.CLASS_NAME, 'more-btn')
        more_btn.click()
        time.sleep(1)
    except:
        print(f'pages = {i}')
        break
        
print('60분후에 프로그램 종료!!, 중지하려면 ctrl+c')
time.sleep(6000)