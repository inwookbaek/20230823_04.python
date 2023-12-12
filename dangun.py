from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys
from bs4 import BeautifulSoup as bs

# 서울%20브롬톤
# search = input('검색단어 => ')
search = sys.argv[1]
condition = sys.argv[2]

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

soup = bs(driver.page_source, 'html.parser')
title = soup.select('.article-title')
region = soup.select('.article-region-name')
price = soup.select('.article-price')
# 
i = 0
while i <= len(title)-1:
    if(condition.casefold() in title[i].text.strip().casefold()):
        print(title[i].text.strip(), region[i].text.strip(), price[i].text.strip())    
    i += 1

print('60분후에 프로그램 종료!!, 중지하려면 ctrl+c')
time.sleep(6000)