import pandas as pd
import glob
from konlpy.tag import Okt
from sklearn.preprocessing import LabelEncoder

# 데이터들을 로딩
datasets = glob.glob('data2.csv')

# 데이터들을 하나로 합침
data_list = []
for data in datasets:
    data_list.append(pd.read_csv(data))
data = pd.concat(data_list, ignore_index=True)

# 말머리를 제외한 데이터들을 하나로 합침
data['나머지'] = data[['제목', '닉네임','본문']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# 말머리에 라벨링 (수동)
mapping = {'일반': 0, '소식': 1, '후기': 2, '팁': 3, 'MOD': 4, '불판': 5}
data['x'] = data['말머리'].map(mapping)

# 나머지에 라벨링 (자동)
encoder = LabelEncoder()
data['y'] = encoder.fit_transform(data['나머지'])
label = encoder.classes_

okt = Okt()

# 문장을 형태소 단위로 파싱
for i in range(len(data['나머지'])):
    data.at[i, '나머지'] = okt.morphs(data.at[i, '나머지']) # 더 효율적인 코드 data['나머지'] = data['나머지'].apply(lambda x: okt.morphs(x))

stopwords = pd.read_csv('../data/stopwords.csv', index_col = 0)
for i in range(len(data['나머지'])): # 나머지에 들어있는 각 문장마다
    print("Original:", data.at[i, '나머지'])
    words = []
    for j in range(len(data.at[i, '나머지'])):
        if len(data.at[i, '나머지'][j]) > 1:   # 글자 1이상의 단어에 대해
            if data.at[i, '나머지'][j] not in list(stopwords['stopword']): # stopwords에 속하지 않는 것만
                words.append(data.at[i, '나머지'][j])  # words리스트에 추가
    print("Filtered:", words)  # 필터링된 단어들을 출력
    data.at[i, '나머지'] = ' '.join(words)

for i in range(10):
    print(data.at[i, '나머지'])


