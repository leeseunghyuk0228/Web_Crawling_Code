from selenium import webdriver as wd
import time
driver = wd.Chrome('/Users/halo8/Desktop/chromedriver')
driver.get('https://www.naver.com')
time.sleep(2)
driver.quit()
