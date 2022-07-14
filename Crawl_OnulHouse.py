# 오늘의집 사이트 질문과 답변 게시글 수집
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import csv
import time
from selenium.webdriver.common.keys import Keys
p=re.compile('@\w*\xa0 |((https|hps|http)://\S*|(https|hps|http)://\S*.com|\r|\u2060|[""\U00010000-\U0010FFFF""]+|ㅋ*|ㅎ*|ㅠ*|ㅜ*|@\w* |(\d+:\d+))',flags=re.UNICODE)
driver = wd.Chrome(executable_path="/Users/halo8/Desktop/양식/chromedriver")
title,text=[],[]

for n in range(1,10):
    url=f'https://ohou.se/questions?query=%EC%9B%90%EB%A3%B8%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4&page={n}'
    driver.get(url)
    time.sleep(5)
    hs=driver.page_source
    hs=bs(hs,'html.parser')

    all_title=hs.find_all('div',class_='css-13xsgfl-QuestionTitle e1amn78m11')
    all_text=hs.find_all('div',class_='css-6kkt2h-QuestionDescription e1amn78m10')
    for i,j in zip(all_title,all_text):
        ti=p.sub(string=i.text,repl='')
        te=p.sub(string=j.text,repl='')
        ti=' '.join(ti.split())
        te=' '.join(te.split())
        title.append(ti)
        text.append(te)
    time.sleep(3)

driver.quit()

