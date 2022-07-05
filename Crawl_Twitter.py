# pip3 install GetOldTweets3
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.common.keys import Keys

urls = 'https://twitter.com/search?q=BTS%20tuckercarlson(lang%3Aen)&src=typed_query&f=top'

driver = wd.Chrome(executable_path="/Users/halo8/Desktop/chromedriver")
driver.get(urls)
last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
html_source = ''

time.sleep(3)

for i in range(0, 5000):
    element = driver.find_element_by_tag_name('body')
    element.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    if i % 3 == 0:
        html_source += driver.page_source
    if i % 30 == 0:
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        if last_page_height == new_page_height:
            break
        last_page_height = new_page_height
time.sleep(3)

html_source += driver.page_source

time.sleep(3)
soup = bs(html_source, "html.parser")
body = soup.find_all('div', class_='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe \
r-bcqeeo r-bnwqim r-qvutc0')
res = []

for idx, i in enumerate(body):
    res.append(i.get_text())
for i in list(set(res))[1:]:
    print('1', i.replace('\n', ''))
driver.close()