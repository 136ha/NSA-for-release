import requests
from bs4 import BeautifulSoup

import time
from datetime import datetime

import numpy as np
import pandas as pd

import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# 경제 데이터 크롤링
daum = []

for n in range(1, 10):
    url = f'https://news.daum.net/breakingnews/economic?page={n}'

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    # title 크롤링
    for link in soup.select('#mArticle > div.box_etc > ul > li > div > strong > a'):
        title = link.string
        daum.append(str(title))

# 정치 데이터 크롤링

for n in range(1, 10):
    url = f'https://news.daum.net/breakingnews/politics?page={n}'

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    # title 크롤링
    for link in soup.select('#mArticle > div.box_etc > ul > li > div > strong > a'):
        title = link.string
        daum.append(str(title))

# 오늘 날짜를 가져온다.
today = datetime.today().strftime("%Y%m%d")

# 경로 / 주소 / 헤더 정의
# https://butnotforme.tistory.com/entry/python으로-업무-자동화까지-8-requests3?category=932590 [butnotforme]
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" }

# 정치 속보
naver = []

for n in range(1, 10):
    url = f'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100&date={today}&page={n}'
    
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    # title 크롤링
    for link in soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt > a'):

        title = link.string
        naver.append(str(title))

# 경제 속보

for n in range(1, 10):
    url = f'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=101&date={today}&page={n}'
    
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    # title 크롤링
    for link in soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt > a'):

        title = link.string
        naver.append(str(title))

url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR%3Ako'

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')
time.sleep(1)

# title 크롤링
google = []

for link in soup.select('h3 > a'):    
    title = link.string
    # print(title)
    google.append(title)

# 서브 주제 크롤링
for link in soup.select('h4 > a'):
    inner = link.string
    # print(inner)
    google.append(inner)

# daum 중복 제거
temp = set(daum)
daum = list(temp)

# google 중복 제거
temp = set(google)
google = list(temp)

# naver 중복 제거
temp = set(naver)
naver = list(temp)

# re를 이용하여 특수문자 제거
dataset = daum + google + naver
temp_data = []

for sentence in dataset:
    temp = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
    temp = re.sub('[\r\n\t]', '', temp)
    temp = re.sub('조선일보', '', temp)
    temp = re.sub('일보', '', temp)
    temp = re.sub('뉴스', '', temp)
    temp = re.sub('중앙', '', temp)

    temp_data.append(temp)
    
# temp_data 중복 제거
temp = set(temp_data)
temp_data = list(temp)

with open(os.path.join(BASE_DIR, 'news.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(temp_data, json_file, ensure_ascii = False, indent='\t')

print('뉴스기사크롤러 끝')

from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import matplotlib.font_manager as fm

# 설치된 폰트 출력
font_list = [font.name for font in fm.fontManager.ttflist]
print(font_list)
font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
print(font_list[:5])

font_family = "Ungraphic.otf"
plt.rcParams["font.family"] = font_family

dataset = temp_data

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
    font_path = '/Library/Fonts/Ungraphic.otf',
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

print("시각화 끝")
