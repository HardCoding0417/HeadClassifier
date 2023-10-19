from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import csv
from datetime import datetime

def url_collector(category_num, page_num):
    pages = [page_num]
    category_list = [0, 330, 20, 340, 350]

    for i in range(1, pages[0]+1):
        G_url = ('https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page={}'
                 .format(category_list[category_num], i))
        driver.get(G_url)
        sleep(2)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        a_tag_list = soup.select('a[href^="/mgallery/board/view/"]')
        url_list = [a_tag['href'] for a_tag in a_tag_list]

        # 리스트의 각 항목을 CSV 파일에 작성
        with open(f"data/url_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            for url in url_list:
                csv_writer.writerow([url])

if __name__ == '__main__':
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/61.0.3163.100 Safari/537.36")
    options = ChromeOptions()
    options.add_argument('user-agent=' + user_agent)
    options.add_argument("lang=ko_KR")

    # 크롬 드라이버 최신 버전 설정
    service = ChromeService(executable_path=ChromeDriverManager().install())

    # chrome driver
    driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

    category = ['Normal', 'News', 'Review', 'Tip', 'Mod']

    url_collector(0,1)
