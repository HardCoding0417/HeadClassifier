from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
from bs4 import BeautifulSoup




def func(t):
    df_titles = pd.DataFrame()
    titles = []
    pages = [1]
    category_list = [0, 330, 20, 340, 350]
    for j in category_list:
        url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page=1'.format(j)
        # print(url)
        for k in range(1, pages[0]+1):
            G_url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page={}'.format(j,k)
            driver.get(G_url)
            time.sleep(0.5)  # 페이지를 바꿀 시간을 줘야한다 없으면 에러가 발생할 수 있음.
            for i in range(2, 47):
                try:
                    title = driver.find_element('xpath',
                                                '//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[{}]/td[3]/a[1]'
                                                .format(i)).text
                    # title = re.compile('').sub('', title))

                    titles.append(title)
                except:
                    print("error {}".format(i))
                df_section_title = pd.DataFrame(titles, columns=['titles'])
                df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
                df_titles.to_csv('../data/head_.csv', index=False)
                titles = []

    for i in range(1, 2):
        driver.get('https://gall.dcinside.com/mgallery/board/lists/?id=mouse&page={}'.format(i))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        links = soup.select('a[href^="/mgallery/board/view/"]')
        for link in links:
            print(f'글 링크: {link}')
        time.sleep(0.5)

    return 0


if __name__ == '__main__':
    url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head=0&page=1'

    options = ChromeOptions()
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument('user-agent=' + user_agent)
    options.add_argument("lang=ko_KR")

    # 크롬 드라이버 최신 버전 설정
    service = ChromeService(executable_path=ChromeDriverManager().install())
    # chrome driver
    driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

    category = ['Normal', 'News', 'Review', 'Tip', 'Mod']

    func(0)






