from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime
from time import sleep
from crawler import scrape
from job1_1 import func

user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

if __name__ == '__main__':
    scrape_list = func(0,1, driver)
    scrape(scrape_list, driver)




