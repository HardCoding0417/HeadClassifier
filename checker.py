import pandas as pd
import glob

def checker(csv_file):
    first_page, last_page = float('inf'), 0  # Initialize to extreme values

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        urls = df['URL'].tolist()

    for url in urls:
        page_num = int(url.split('page=')[-1])
        first_page = min(first_page, page_num)
        last_page = max(last_page, page_num)

    return first_page, last_page

if __name__ == '__main__':
    csv_files = glob.glob('data/url_*.csv')
    first_page, last_page = checker(csv_files)

    crawl_start = last_page + 1
    crawl_end = crawl_start + 10

    for page_num in range(crawl_start, crawl_end):
        pass









