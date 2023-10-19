from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime
from time import sleep
from contents_scraper import scrape
import csv


user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url_lists = []
with open('data/url_Mod.csv', 'r', encoding='UTF-8-sig') as csvfile:
    for url_list in csvfile:
        url_lists.append(url_list)

if __name__ == '__main__':
    scrape(url_lists, driver)
    driver.quit()




