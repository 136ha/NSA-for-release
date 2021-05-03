import re
import os
import time
import json
import sys
from konlpy.tag import Okt
from collections import Counter
import numpy as np
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import streamlit as st

from wordcloud import WordCloud
# import streamlit_wordcloud as wordcloud
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

import matplotlib.font_manager as fm

font_family = "UnBatang"
plt.rcParams["font.family"] = font_family

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'news.json'), 'r') as f:
    json_data = json.load(f)

dataset = json_data

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
    font_path = '/usr/share/fonts/truetype/unfonts-core/UnBatang.ttf',
    background_color='white',
    colormap = 'Accent_r',
    width = 800,
    height = 800
)

# temp_list = []
# for keys, values in words.items():
#     temp_dict = dict(text=keys, value=values)
#     temp_list.append(temp_dict)

wordcloud_words = wordcloud.generate_from_frequencies(words)

array = wordcloud.to_array()

fig = plt.figure(figsize=(6, 6))
plt.imshow(array, interpolation="bilinear")
plt.axis('off')
# plt.show()

fig.savefig(BASE_DIR + 'business_anlytics_worldcloud.png')

# return_obj = wordcloud.visualize(temp_list, tooltip_data_fields={'text':'word', 'value':'count'}, per_word_coloring=True)

# hue값은 항상 변수가 적은 것으로 해야 이쁨.
data = pd.DataFrame(noun_adj_adv_list, columns=['words'])

path = '/usr/share/fonts/truetype/unfonts-core/UnDotum.ttf'
fontprop = fm.FontProperties(fname=path, size=18)
plt.figure(figsize=(6,6))
sns.set_palette("pastel")
ax = sns.countplot(x='words', data=data, order=data['words'].value_counts()[:12].index)
plt.title('Top 12 뉴스 키워드 순위', fontsize=12, fontproperties=fontprop)
plt.xlabel('뉴스 키워드', fontsize=12, fontproperties=fontprop)
plt.ylabel('누적 개수', fontsize=12, fontproperties=fontprop)
plt.xticks(fontsize=8, fontproperties=fontprop)
sns.despine()

ax.figure.savefig(BASE_DIR + "business_anlytics_bar.png")
