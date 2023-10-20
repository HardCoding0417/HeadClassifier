import pandas as pd
import glob
import datetime

# data_path = glob.glob('../MoonJeangHwan/*.csv')
data_path = glob.glob('../crawling_data/DC_prd.csv')
# 해당 경로를 집어넣고 이를 리스트로 반환, 와일드카드를 사용하여 여러 csv파일을 concat하기 위해 glob을 사용
print(data_path)

df = pd.DataFrame() # 빈 데이터 프레임 생성 -> concat을 위함
for path in data_path:
    df_temp = pd.read_csv(path) # df_temp 임시 데이터프레임을 생성, glob한 경로를
    df = pd.concat([df, df_temp])
print(df.head())
# print(df['titles'].value_counts())
df.info()
df.to_csv('../crawling_data/dcinside_{}.csv'.format(
    datetime.datetime.now().strftime('%m%d')), index=False, encoding='UTF-8-sig')