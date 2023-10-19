import pandas as pd
import glob
import datetime

# data_path = glob.glob('../MoonJeangHwan/*.csv')
data_path = glob.glob('../crawling_data/DC_v2.csv')
print(data_path)

df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp])
print(df.head())
# print(df['titles'].value_counts())
df.info()
df.to_csv('../crawling_data/dcinside_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False, encoding='UTF-8-sig')