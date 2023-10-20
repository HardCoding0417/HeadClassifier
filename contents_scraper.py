from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
from time import sleep
import os
import threading

# get 10초 이상 막히면 False를 반환
def get_with_timeout(driver, url, timeout=10):
    def load_url():
        driver.get(url)

    thread = threading.Thread(target=load_url)
    thread.start()
    thread.join(timeout=timeout)

    if thread.is_alive():
        print(f"get작업이 10초 이상 지연되고 있습니다 {url}")
        return False

    return True

# 중복방지를 체크하는 함수
def load_scraped_links(file_path):
    scraped_links = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='UTF-8-sig') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                scraped_links.add(row['글 링크'])
    return scraped_links

def scrape(links, driver, scraped_links, save_path):
    failed_count = 0
    file_exists = os.path.exists(save_path)  # 파일이 존재하는지 체크

    # 링크 리스트를 순회하며 파싱. text를 따옴
    for link in links[1:]:
        data = []
        if link in scraped_links:
            print(f"{link}은(는) 이미 스크래핑되었습니다.")
            continue

        result = get_with_timeout(driver, 'https://gall.dcinside.com/' + link, timeout=10)
        if not result is True:
            print(f"링크 {link}에 접속하는 데 10초 이상 소요되었습니다.")
            driver.quit()

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
        scraped_links.add(link)

        # csv로 저장
        if len(data) > 0:
            keys = data[0].keys()
            with open(save_path, 'a', newline='', encoding='UTF-8-sig') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                # 파일이 존재하지 않을 때만 헤더를 씀
                if not file_exists:
                    dict_writer.writeheader()

                for gall_post in data:
                    dict_writer.writerow(gall_post)
        else:
            print("No data to write")


if __name__ == '__main__':
    user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    lis = ['https://gall.dcinside.com/mgallery/board/view/?id=mouse&no=654581&page=1',
           'https://gall.dcinside.com/mgallery/board/view/?id=mouse&no=654579&page=1',
           'https://gall.dcinside.com/mgallery/board/view/?id=mouse&no=654548&page=1']
    print(scrape(lis, driver))

