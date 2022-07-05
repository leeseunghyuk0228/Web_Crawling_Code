# 특정 한 곳 리뷰 수집하기 #
import time
from selenium import webdriver as wd

driver=wd.Chrome('/Users/halo8/Desktop/chromedriver')
driver.get('https://domestic-order-site.yanolja.com/review/properties/27908/reviews')
driver.set_window_size(1920,1080)
time.sleep(1)
fh=driver.execute_script("return document.documentElement.scrollHeight")
while 1:
    driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    lh=driver.execute_script("return document.documentElement.scrollHeight")
    if fh==lh: break
    else: fh=lh
time.sleep(3)
driver.quit()

## 특정 지역 내 업체 수집 비교하기 ##
import pandas as pd
import time
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import re

driver = wd.Chrome('/Users/halo8/Desktop/chromedriver')
driver.get('https://www.yanolja.com/')

area = '부평역'
# 검색창 클릭
search = driver.find_element_by_css_selector('#__next > section > header > div > a.HomeSearchBar_search__2wDcY')
wd.ActionChains(driver).click(search).perform()
time.sleep(1)

# 날짜 입력(수동)
driver.find_element_by_css_selector(
    '#__next > div.SunnyLayout_container__3PLag.search_layout__1Gv7E > header > nav > div.SearchNavBody_wrap__10bPS > form > div.SearchInput_filters__11V9m > button.NavFilterButton_container__20Hr2.NavFilterButton_collapse__3JGvV.SearchInput_calendarButton__3sNMZ').click()
driver.find_element_by_css_selector(
    'body > div:nth-child(44) > div > div > section > section:nth-child(3) > div').click()
time.sleep(20)

# 검색어 입력
search_box = driver.find_element_by_css_selector(
    '#__next > div.SunnyLayout_container__3PLag.search_layout__1Gv7E > header > nav > div.SearchNavBody_wrap__10bPS > form > div.SearchInput_inputWrap__1KJjw > input')
wd.ActionChains(driver).click(search_box).send_keys(f'{area}').send_keys(Keys.ENTER).perform()
time.sleep(10)

fh = driver.execute_script("return document.documentElement.scrollHeight")
for i in range(1, 10):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
time.sleep(5)

while 1:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(10)
    lh = driver.execute_script("return document.documentElement.scrollHeight")
    if lh == fh:
        break
    else:
        lh = fh

hs = driver.page_source
hss = bs(hs, 'html.parser')

## 이름, 별점, 리뷰개수, 가격
name, star, review, mh, price = [], [], [], [], []

for n in hss.find_all('strong', class_='PlaceListTitle_text__2511B'):
    name.append(n.text)
for s in hss.find_all('div', class_='PlaceListScore_container__2-JXJ PlaceListItemText_score__1O-nW'):
    if len(s) == 2:
        star.append(s.text[:3])
        review.append(s.text[4:-1].replace(',', ''))
    else:
        star.append(0)
        review.append(0)
for m in hss.find_all('div', class_='PlaceListGrade_container__1oIhJ'):
    mh.append(m.text)

# 대실 시간, 비용, 숙박 시간, 비용
half_time = []
half_price = []
full_time = []
full_price = []

for p in hss.find_all('div', class_='PlaceListItemText_prices__2_1nN'):
    m = re.search('(\d*시간\d*,\d*원)', p.text)
    if m:
        sentence = p.text[m.start():m.end()]
        half_time.append(sentence.split('시간')[0])
        half_price.append(sentence.split('시간')[1])
    else:
        half_time.append(p.text)
        half_price.append(p.text)

    m = re.search('(\d*:\d*부터\d*,\d*원)', p.text)
    if m:
        sentence = p.text[m.start():m.end()]
        full_time.append(sentence.split('부터')[0])
        full_price.append(sentence.split('부터')[1])
    else:
        full_price.append(p.text)
        full_time.append(p.text)

s = len(name)
for n in [mh, star, review, full_time, full_price, half_time, half_price]:
    if s > len(n): s = len(n)
s -= 1

df = pd.DataFrame({'name': name[:s], 'type': mh[:s], 'star': star[:s], 'review_cnt': review[:s], '대실시간': half_time[:s],
                   '대실비용': half_price[:s], '숙박시간': full_time[:s], '숙박비용': full_price[:s]})

df.star = df.star.astype(float)
df.review_cnt = df.review_cnt.astype(float)
df['cnt/star'] = df.review_cnt / df.star
df.to_excel(f'/Users/halo8/Desktop/{area}.xlsx')

driver.quit()
