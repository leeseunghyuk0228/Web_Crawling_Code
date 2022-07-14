# 다음 기사 댓글 수집
import time,re
from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd

p=re.compile('@\w*\xa0 |((https|hps|http)://\S*|(https|hps|http)://\S*.com|\r|\u2060|[""\U00010000-\U0010FFFF""]+|ㅋ*|ㅎ*|ㅠ*|ㅜ*|@\w* |(\d+:\d+))',flags=re.UNICODE)

url = 'https://news.v.daum.net/v/20211122075529484'

driver = wd.Chrome(executable_path="/Users/halo8/Desktop/양식/chromedriver")
# 매개변수의 주소 띄움
driver.get(url)
#크롤링에 필요 없는 특정 element의 속성 제거하기(스포츠란)
time.sleep(5)
# 다음뉴스의 모든 댓글 페이지를 띄움
cnt = 0
err_cnt=0
while cnt < 600:
    try:
        print(cnt)
        driver.find_element_by_css_selector(
            "#alex-area > div > div > div > div.cmt_box > div.alex_more > button"
            ).click()
        time.sleep(1.5)
        cnt += 1
    except:
        err_cnt+=1
        if err_cnt==30:
            break
        else:
            pass
html_source = driver.page_source
driver.quit()


hs=bs(html_source,"html.parser")
a=hs.find_all('p',class_='desc_txt font_size_17')

data=[]
for i in a:
    t=i.text.replace('\n',' ')
    t=' '.join(t.split())
    data.append(p.sub(string=t,repl=''))