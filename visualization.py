import os
import json
from konlpy.tag import Okt
from collections import Counter
from tqdm import tqdm
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import matplotlib.font_manager as fm

# 설치된 폰트 출력
font_list = [font.name for font in fm.fontManager.ttflist]
print(font_list)

font_family = "gothic"
plt.rcParams["font.family"] = font_family

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'news.json'), 'r') as f:
    json_data = json.load(f)

dataset = list(json.dumps(json_data))

# 형태소 분석
okt = Okt() 
morphs = [] 

for sentence in dataset: 
    morphs.append(okt.pos(sentence)) 
# print(morphs[:5])

# 명사 추출
noun_adj_adv_list=[] 
for sentence in morphs : 
    for word, tag in sentence : 
        if tag in ['Noun'] and ("것" not in word) and ("내" not in word)and ("나" not in word)and ("수"not in word) and("게"not in word)and("말"not in word): 
            noun_adj_adv_list.append(word) 

# print(noun_adj_adv_list[:50])

# 한 글자인 단어들 삭제
noun_adj_adv_list = [x for x in noun_adj_adv_list if len(x)>1]


count = Counter(noun_adj_adv_list)
words = dict(count.most_common())
wordcloud = WordCloud(
    font_path = 'malgun.ttf',
    background_color='white',
    colormap = 'Accent_r',
    width = 800,
    height = 800
)

wordcloud_words = wordcloud.generate_from_frequencies(words)

array = wordcloud.to_array()

fig = plt.figure(figsize=(6, 6))
plt.imshow(array, interpolation="bilinear")
plt.axis('off')
plt.show()

fig.savefig(os.path.join(BASE_DIR, 'business_anlytics_worldcloud.png'))

# hue값은 항상 변수가 적은 것으로 해야 이쁨.
data = pd.DataFrame(noun_adj_adv_list, columns=['words'])

plt.figure(figsize=(6,6))
sns.set_palette("pastel")
ax = sns.countplot(x='words', data=data, order=data['words'].value_counts()[:12].index)
ax.set_title('Top 12 뉴스 키워드 순위', fontsize=12)
ax.set_xlabel('뉴스 키워드', fontsize=12)
ax.set_ylabel('누적 개수', fontsize=12)
ax.tick_params(labelsize=8)
sns.despine()

ax.figure.savefig(os.path.join(BASE_DIR, "business_anlytics_bar.png"))

