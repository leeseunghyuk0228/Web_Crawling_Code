def you(urls, category='카테고리'):
    from selenium import webdriver as wd
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    import re
    import time
    from selenium.webdriver.common.keys import Keys
    p = re.compile('@\w*\xa0 |\n|((https|hps|http)://\S*|(https|hps|http)://\S*.com|\r|\u2060|[""\U00010000-\U0010FFFF""]+|ㅋ*|ㅎ*|ㅠ*|ㅜ*|@\w* |(\d+:\d+))',flags=re.UNICODE)
    options = wd.ChromeOptions()
    options.add_argument('window-size=1920x1080')  # 크롬드라이버 창크기
    options.add_argument("headless")  # 창 숨기기
    options.add_argument('disable-gpu')  # 그래픽 성능 낮춰서 크롤링 성능 높아기
    options.add_argument('lang=ko_KR')

    driver = wd.Chrome(executable_path="/Users/halo8/Desktop/chromedriver")
    driver.get(urls)
    time.sleep(1.5)
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.execute_script("window.scrollTo(0, 700);")
    time.sleep(0.8)

    while 1:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.5)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height

    time.sleep(1)
    buttons = driver.find_elements_by_css_selector("#more-replies > a")
    for button in buttons:
        try:
            button.send_keys(Keys.ENTER)
            time.sleep(0.5)
            button.click()
        except:
            pass
    time.sleep(10)

    title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
    cn = driver.find_element_by_xpath('//*[@id="text"]/a').text
    lk = driver.find_elements_by_xpath('//*[@id="vote-count-middle"]')
    dt = driver.find_elements_by_xpath('//*[@id="header-author"]/yt-formatted-string/a')
    cname, text, like, date = [], [], [], []

    hs = driver.page_source
    hs2 = bs(hs, 'html.parser')

    for i in hs2.find_all('yt-formatted-string', id='content-text'):
        tt = i.find_all('span')
        if len(tt) > 0:
            s = ''
            for t in tt:
                s += t.get_text()
            text.append(p.sub(string=s, repl='').strip())
        else:
            text.append(p.sub(string=i.get_text(), repl='').strip())

    for j in lk:
        like.append(j.text)
        cname.append(cn)

    for d in dt:
        date.append(d.text)

    driver.quit()
    label = [title for _ in range(len(text))]
    channel = ['youtube' for _ in range(len(text))]
    category = [category for _ in range(len(text))]
    df = pd.DataFrame(
        {'label': label, 'text': text, 'date': date, 'like': like, 'string_카테고리': category, 'string_채널명': cname,
         'channel': channel})
    try:
        df.to_excel('/' + title + '.xlsx')
    except:
        df.to_excel('/' + urls[32:] + '.xlsx')
    return