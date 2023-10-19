from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import pandas as pd
import datetime
from time import sleep

# 중복 체크를 위한 함수
def checker(csv_files):
    first_page = float('inf')
    last_page = 0

    # csv파일들을 불러와서 파이썬 리스트화
    all_urls = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        urls = df['URL'].tolist()
        all_urls.extend(urls)

    # 글 번호를 추출해서 제일 작은 번호와 큰 번호를 반환
    for url in all_urls:
        page_num = int(url.split('page=')[-1])
        first_page = min(first_page, page_num)
        last_page = max(last_page, page_num)

    return first_page, last_page

def scrape(links, driver):
    data = []

    # 링크 리스트를 순회하며 파싱. text를 따옴
    for link in links:
        try:
            driver.get(link)
        except:
            print("링크에 접속하지 못했습니다.")
        sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        gall_num = soup.select('td.gall_num')
        headtext = soup.select('span.title_headtext')
        title = soup.select('span.title_subject')
        nickname = soup.select('span.nickname em')
        main_txt = soup.select('div.write_div')

        for gall_num, headtext, title, nickname, main_txt in zip(gall_num, headtext, title, nickname,main_txt):
            # mongoDB에도 적합하도록 딕셔너리 형태로 저장
            gall_post = {
                # '글 번호': gall_num.text,
                '말머리': headtext.text,
                '제목': title.text,
                '닉네임': nickname.text,
                '본문': main_txt.text,
                '글 링크': link
            }
            data.append(gall_post)

    # csv로 저장
    keys = data[0].keys()
    with open('MoonJeangHwan/data.csv', 'w', newline='', encoding='UTF-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        for gall_post in data:
            dict_writer.writerow(gall_post)




if __name__ == '__main__':
    user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    lis = ['https://gall.dcinside.com/mgallery/board/view/?id=mouse&no=654581&page=1',
           'https://gall.dcinside.com/mgallery/board/view/?id=mouse&no=654579&page=1',
           'https://gall.dcinside.com/mgallery/board/view/?id=mouse&no=654548&page=1']
    print(scrape(lis, driver))


# for i in range(1, 2):
#     driver.get('https://gall.dcinside.com/mgallery/board/lists/?id=mouse&page={}'.format(i))
#     page_source = driver.page_source
#     soup = BeautifulSoup(page_source, 'html.parser')
#     links = soup.select('a[href^="/mgallery/board/view/"]')
#     return links
