from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime
from time import sleep

def scrape(links):
    data = []
    for link in links:
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        gall_num = soup.select('td.gall_num')
        headtext = soup.select('span.title_headtext')
        title = soup.select('span.title_subject')
        nickname = soup.select('span.nickname em')
        main_txt = soup.select('div.write_div')

        # mongoDB에도 적합하도록 딕셔너리 형태로 저장
        record = {
            '글 번호': gall_num.text if gall_num else '',
            '말머리': headtext.text if headtext else '',
            '제목': title.text if title else '',
            '닉네임': nickname.text if nickname else '',
            '본문': main_txt.text if main_txt else '',
            '글 링크': link
        }
        data.append(record)
        sleep(0.5)
    return data

user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#
# for i in range(1, 2):
#     driver.get('https://gall.dcinside.com/mgallery/board/lists/?id=mouse&page={}'.format(i))
#     page_source = driver.page_source
#     soup = BeautifulSoup(page_source, 'html.parser')
#     links = soup.select('a[href^="/mgallery/board/view/"]')
#     for link in links:
#         scrape(link)
#         print(f'글 링크: {link}')
#     sleep(0.5)
#
