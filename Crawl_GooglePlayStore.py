from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import csv
import time
from selenium.webdriver.common.keys import Keys
p=re.compile('@\w*\xa0 |((https|hps|http)://\S*|(https|hps|http)://\S*.com|\r|\u2060|[""\U00010000-\U0010FFFF""]+|ㅋ*|ㅎ*|ㅠ*|ㅜ*|@\w* |(\d+:\d+))',flags=re.UNICODE)
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')#크롬드라이버 창크기
# options.add_argument("headless") #창 숨기기
options.add_argument('disable-gpu') #그래픽 성능 낮춰서 크롤링 성능 높아기
options.add_argument('lang=ko_KR')
driver = wd.Chrome(executable_path="/Users/halo8/Desktop/chromedriver")

url = 'https://play.google.com/store/apps/details?id=com.samsungcard.pet&hl=ko&gl=US&showAllReviews=true'

driver.get(url) #크롤링할 유튜브 영상 url

last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

while 1:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        time.sleep(2)
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height

#정보 추출하기
html_source = driver.page_source
soup = bs(html_source, 'lxml')
# review = soup.find_elements_by_xpath("//span[@jsname='bN97Pc']")
reviews = soup.find_all('span', {'jsname':'bN97Pc'})
print(len(reviews))
for review in reviews:
    print(review.text)