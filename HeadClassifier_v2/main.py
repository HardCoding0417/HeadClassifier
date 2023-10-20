from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime
from time import sleep
from contents_scraper import scrape
from contents_scraper import load_scraped_links
import csv


user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url_list = []
with open('data/urls.csv', 'r', encoding='UTF-8-sig') as csvfile:
    for url in csvfile:
        url_list.append(url)

input_file_path = load_scraped_links('data.csv')

if __name__ == '__main__':
    # def scrape(links, driver, scraped_links, save_path):
    scrape(url_list, driver, scraped_links=input_file_path, save_path='data/data.csv')
    driver.quit()





