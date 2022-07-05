import random
import re
import urllib.parse
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
op=re.compile('\r|\n|\t|Color:|Ships From:|Logistics:')
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}

feedback_uri = "https://feedback.aliexpress.com/display/productEvaluation.htm"

owenerMemberID='2'+str(random.choice(range(0,9)))
companyID='2'+str(random.choice(range(0,9)))

params = {
            'productId': '1005003721587630',
            'v': 2,
            'ownerMemberId': owenerMemberID,
            'companyId': companyID,
            'memberType': 'Seller',
            'i18n': 'true' if False else 'false',
            'translate': 'Y' if True else 'N',
            'onlyFromMyCountry':  'true' if False else 'false',
            'withPictures':  'true' if False else 'false',
            'page': 1
        }

url = f"{feedback_uri}?{urllib.parse.urlencode(params)}"
response=requests.post(url,params=params)
res=requests.get(url,headers=headers)
hs1=bs(res.text,'html.parser')
base_url=url[:-1]

star,option1,option2,option3,text,date,Help_Y,Help_N=[],[],[],[],[],[],[],[]

for u in range(1,15):
    page_url=base_url+str(u)
    res=requests.get(url,headers=headers)
    hs1=bs(res.text,'html.parser')
    for i in hs1.find_all('div',class_='fb-main'):
        d=i.find_all('span')
        star.append(int(re.findall('\d{1,3}',d[0].find('span')['style'])[0])/20)
        option1.append(op.sub(string=d[2].text,repl=''))
        option2.append(op.sub(string=d[3].text,repl=''))
        option3.append(op.sub(string=d[4].text,repl='').strip())
        text.append(op.sub(string=d[5].text,repl='').strip())
        date.append(op.sub(string=d[6].text,repl=''))
        Help_Y.append(i.find_all('span',class_='thf-digg-num')[0].text.strip())
        Help_N.append(i.find_all('span',class_='thf-digg-num')[1].text.strip())

df=pd.DataFrame({'text':text,'op1':option1,'op2':option2,'op3':option3,'star':star,'date':date,'Help_Y':Help_Y,'Help_N':Help_N})