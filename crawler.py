import requests
from bs4 import BeautifulSoup

from datetime import datetime
import numpy as np
import pandas as pd
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print('뉴스기사크롤러 시작')

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

for n in tqdm(range(1, 10)):
    url = f'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100&date={today}&page={n}'
    
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    # title 크롤링
    for link in soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt > a'):

        title = link.string
        naver.append(str(title))

# 경제 속보

for n in tqdm(range(1, 10)):
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
