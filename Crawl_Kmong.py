from selenium import webdriver as wd
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
content={}
urllist=[]
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
for num in range(1,9):
    url=f'https://kmong.com/search?type=gigs&page={num}&sort=_score&service=web&metadata=&keyword=%ED%81%AC%EB%A1%A4%EB%A7%81&q=%ED%81%AC%EB%A1%A4%EB%A7%81'
    res=requests.get(url=url,headers=headers)
    re=bs(res.content,'html.parser')
    for u in re.find_all('a',class_='css-j9gtx5 eu87mqk0'):
        urllist.append('https://kmong.com'+u.get('href'))

print(len(urllist))

for idx, ul in enumerate(urllist):
    res = requests.get(url=ul, headers=headers)
    re = bs(res.content, 'html.parser')
    sec = re.find('section', class_='css-1evz4lj ev4y9ek0')
    data = []
    try:
        for j, k in zip(sec.find_all('div', class_='css-vpdlzv e18kysmh2'),
                        sec.find_all('span', class_='css-1r5ofwa ev4y9ek10')):
            data.append(j.text.replace('\n', '')), data.append(k.text)
        content[f'{str(idx)}'] = data
    except:
        pass

standard_func, standard_price = [], []
deluxe_func, deluxe_price = [], []
premium_func, premium_price = [], []

for i in content.keys():
    d = content[str(f'{i}')]
    standard_func.append(d[0])
    standard_price.append(d[1])
    deluxe_func.append(d[2])
    deluxe_price.append(d[3])
    premium_func.append(d[4])
    premium_price.append(d[5])

df = pd.DataFrame(
    {'STANDARD_기능': standard_func, 'STANDARD_가격': standard_price, 'DELUXE_기능': deluxe_func, 'DELUXE_가격': deluxe_price,
     'PREMIUM_기능': premium_func, 'PRMIUM_가격': premium_price})

df.to_excel('/Users/halo8/Desktop/크몽.xlsx')