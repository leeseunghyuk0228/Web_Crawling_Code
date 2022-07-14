# 네이버 카페 검색후 n 개 페이지 크롤링
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
urls=[]
driver=wd.Chrome('/Users/halo8/Desktop/chromedriver')


for n in range(1,10):
    url=f'https://section.cafe.naver.com/ca-fe/home/search/articles?q=%EC%97%AC%EB%A6%84%20%ED%9C%B4%EA%B0%80&p={n}&em=1&pr=3&in=%EA%B0%91%EB%8B%88%EB%8B%A4,%20%EA%B0%80%EB%A0%A4%EA%B5%AC%EC%9A%94,%20%ED%9B%84%EA%B8%B0,%20%EA%B3%84%ED%9A%8D'
    driver.get(url)
    time.sleep(1.5)
    hs=driver.page_source
    hs=bs(hs,'html.parser')
    for i in hs.select('#mainContainer > div > div.SectionSearchContent > \
    div.section_search_content > div > div.article_list_area')[0].find_all('div',class_='detail_area'):
        urls.append(i.find('a').get('href'))
    time.sleep(0.8)
    print(len(urls))

data_a={}

# 각 URL 제목, 게시글, 댓글 수집
for idx,u in enumerate(urls):
    try:
        driver.get(u)
        time.sleep(0.8)
        driver.switch_to.frame('cafe_main')
        time.sleep(1)
        hs=driver.page_source
        hs=bs(hs,'html.parser')
        #카페명
        name=hs.find('strong',class_='cafe_name').text.replace('\n','')
        #제목
        tit=hs.select('#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > h3')[0].text
        #본문
        values=[]
        content=hs.select('#app > div > div > div.ArticleContentBox > div.article_container > div.article_viewer > div > div.content.CafeViewer > div > div')[0].text
        values.append(content.replace('\n',''))
        #댓글
        for r in hs.find_all('span',class_='text_comment'):
            values.append(r.text.replace('\n',''))
        key=name+'제목: '+tit.replace('\n','').replace('\u200b','').strip()+'날짜: '+hs.find('span',class_='date').text[:4]
        data_a[key]=values

    except:
        pass
driver.quit()

# 리스트 추가, 데이터 저장
title,text,channel,date=[],[],[],[]
for i,j in zip(data_a.keys(),data_a.values()):
    for d in j:
        channel.append((i.split('제목: ')[0]))
        title.append(i.split('제목: ')[1].split('날짜: ')[0])
        text.append(d)
        date.append(i.split('날짜: ')[1])

df=pd.DataFrame({'title':title,'text':text,'channel':channel,'date':date})
df.to_excel('/Users/halo8/Desktop/여름휴가_카페.xlsx')