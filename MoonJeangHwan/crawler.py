from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime
from time import sleep

user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


for i in range(1, 2):
    driver.get('https://gall.dcinside.com/mgallery/board/lists/?id=mouse&page={}'.format(i))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    links = soup.select('a[href^="/mgallery/board/view/"]')
    for link in links:
        print(f'글 링크: {link}')
    sleep(0.5)


