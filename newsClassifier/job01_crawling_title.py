from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['General', 'News', 'Reviews', 'Tips', 'MOD']
category_list = [0, 330, 20, 340, 350]

url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head=0&page=1'

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

pages = [3]
titles=[]

df_titles = pd.DataFrame()

for j in category_list:
    url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page=1'.format(j)
    print(url)
    for k in range(1, pages[0]+1):
        G_url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page={}'.format(j,k)
        driver.get(G_url)
        time.sleep(0.5)  # 페이지를 바꿀 시간을 줘야한다 없으면 에러가 발생할 수 있음.
        for i in range(2, 47):
            try:
                title = driver.find_element('xpath',
                                            '//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[{}]/td[3]/a[1]'.format(i)).text
                # title = re.compile('').sub('', title))
                #          # ('[^가-힣]]').sub('', title))
                titles.append(title)
            except:
                print("error {}".format(i))
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
            df_titles.to_csv('../crawling_data/head_.csv', index=False)
            titles = []

# https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head=0&page=1                 일반
# https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head=330&page=1   소식
# https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head=20&page=1    후기
# https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head=340&page=1   팁
# https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head=350&page=1   모드


