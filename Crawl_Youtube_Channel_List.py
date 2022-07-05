from selenium import webdriver as wd
import re
import time

p = re.compile('@\w*\xa0 |\n|((https|hps|http)://\S*|(https|hps|http)://\S*.com|\r|\u2060|[""\U00010000-\U0010FFFF""]+|ㅋ*|ㅎ*|ㅠ*|ㅜ*|@\w* |(\d+:\d+))',flags=re.UNICODE)
driver = wd.Chrome(executable_path="/Users/halo8/Desktop/chromedriver")
driver.get('https://www.youtube.com/user/HicarHilife/videos')
time.sleep(1.5)
last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
while 1:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.5)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height

u = driver.find_elements_by_xpath('//*[@id="metadata-line"]/span[1]')
uu = []
for i in u:
    uu.append(i.text)

num = 0
for i in uu:
    ss = i[4:-1]
    if '천' in ss:
        ss = re.sub(string=ss, pattern='천', repl='000')
    elif '만' in ss:
        ss = re.sub(string=ss, pattern='만', repl='0000')
    print(i.split(' ')[1])
