from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import re
import glob
from datetime import datetime


def extract_post_number(url):
    # 정규 표현식을 사용하여 글 번호 추출
    match = re.search(r'no=(\d+)', url)
    if match:
        return match.group(1)
    return None

def url_collector(category_num, page_num, start_page=1, collected_post_numbers=set(), save_path='data/urls.csv'):
    # param: 카테고리 번호, 페이지 번호, 이미 수집한 urls 파이썬 리스트(중복체크용)
    # csv를 읽어서 toset()를 사용해 파이썬 set화 시킨 뒤 collected_urls로 전달해줘야함
    pages = [page_num]
    category_list = [0, 330, 20, 340, 350]
    all_urls = []

    for i in range(0, pages[0]+1):
        G_url = ('https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page={}'
                 .format(category_list[category_num], i+start_page))
        driver.get(G_url)
        sleep(2)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        a_tag_list = soup.select('a[href^="/mgallery/board/view/"]')
        url_list = [a_tag['href'] for a_tag in a_tag_list]

        # 중복체크
        post_numbers = [extract_post_number(url) for url in url_list]
        new_post_numbers = [pn for pn in post_numbers if pn not in collected_post_numbers]
        # 추출한 글 번호를 all_urls에 추가
        all_urls.extend([url for url, pn in zip(url_list, post_numbers) if pn in new_post_numbers])
        # 수집한 글 번호를 collected_post_numbers에 추가
        collected_post_numbers.update(new_post_numbers)

        # 업데이트된 collected_post_numbers를 저장
        # DataFrame 생성
        df = pd.DataFrame(list(collected_post_numbers), columns=['collected_post_numbers'])
        # CSV 파일로 저장
        df.to_csv(f"data/collected_post_numbers.csv", index=False)

        # 'https://gall.dcinside.com/error/adult' 문자열을 포함한 사이트를 제외합니다
        exclude_substring = 'https://gall.dcinside.com/error/adult'
        # 특정 문자열을 포함하는 URL을 제외하고 수집
        filtered_urls = [url for url in all_urls if exclude_substring not in url]

        final_urls = []
        final_urls.extend(filtered_urls)

        # 스크랩한 데이터를 저장
        # DataFrame 생성
        df = pd.DataFrame(final_urls, columns=['URL'])
        # CSV 파일로 저장
        df.to_csv(f"data/urls_{save_path}.csv", index=False)




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

    try:
        a = pd.read_csv("data/collected_post_numbers.csv")
        collected_post_numbers = set(a['collected_post_numbers'])
    except FileNotFoundError:
        collected_post_numbers = set()

    url_collector(0, 1000, start_page=1, collected_post_numbers=collected_post_numbers)

