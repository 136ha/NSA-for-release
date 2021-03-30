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
import FinanceDataReader as fdr
from bs4 import BeautifulSoup
import requests
import streamlit as st

from wordcloud import WordCloud
import streamlit_wordcloud as wordcloud
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

import matplotlib.font_manager as fm

# 설치된 폰트 출력
# font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
# st.write(font_list)

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
# wordcloud = WordCloud(
#     font_path = '/usr/share/fonts/truetype/unfonts-core/UnBatang.ttf',
#     background_color='white',
#     colormap = 'Accent_r',
#     width = 800,
#     height = 800
# )

temp_list = []
for keys, values in words.items():
    temp_dict = dict(text=keys, value=values)
    temp_list.append(temp_dict)

# wordcloud_words = wordcloud.generate_from_frequencies(words)

# array = wordcloud.to_array()

# fig = plt.figure(figsize=(6, 6))
# plt.imshow(array, interpolation="bilinear")
# plt.axis('off')
# plt.show()

# fig.savefig('business_anlytics_worldcloud.png')

return_obj = wordcloud.visualize(temp_list, tooltip_data_fields={'text':'word', 'value':'count'}, per_word_coloring=True)

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

# ax.figure.savefig("business_anlytics_bar.png")

# streamlit
st.title('실시간 뉴스 키워드 분석')
st.write('실시간으로 14개의 방송사, 10개의 신문사 등을 확인하며 뉴스를 읽어 주요 키워드를 도출하고 그에 맞는 테마주를 추천하는 것을 목표로 하고있습니다. \
    꼭 추천종목에 주의를 가질 필요 없이, 실시간으로 한국 뉴스의 거시적인 동향을 파악하는데 도움이 될 것입니다.')
st.pyplot(plt)

st.write('상위 12개의 키워드만으로는 아쉬울 수 있기 때문에 wordcloud image를 첨부해 두겠습니다. font 크기가 클 수록 중요도가 높은 키워드이며, \
    많은 키워드를 살펴볼 수 있다는 장점이 있습니다. 여러모로 유용하게 사용이 될 수 있다면 좋겠습니다.')
# st.pyplot(ax.figure)
st.write(return_obj)

# 뉴스 분석하기
politician_list = ['대북', '김정은', '북한', '윤석열', '황교안', '이재명', '유시민', '박영선', '유승민', '이낙연', '안철수', '추미애', '오세훈']

st.title('현재 변동폭 주의 테마주 리스트')

# 각 정치인 테마주
north_korea = {'현대로템':'064350', '아난티':'025980', '빅텍':'065450', '현대엘리베이':'017800', '대아티아이':'045390',
                '한창':'005110', '일신석재':'007110', '조비':'001550', '부산산업':'011390', '아시아종묘':'154030'}

yoon_seok_yeol = {'서연':'007860', '덕성':'004830', '모베이스':'101330', '모베이스전자':'012860', '아이크래프트':'052460',
                '서연이화':'200880', '대영포장':'014160', 'NE능률':'053290', '태양금속':'004100'}

hwang_gyo_an = {'한창제지':'009460', '남선알미늄':'008350', '서연탑메탈':'019770', '아세아텍':'050860', '인터엠':'017250',
                '국일신동':'060480', '한송네오텍':'226440'}

lee_jae_myung = {'에이텍':'045660', '에이텍티앤':'224110', '동신건설':'025950', '비비안':'002070', '오리엔트정공':'065500'}

yoo_si_min = {'sg충방':'001380', '와이비엠넷':'057030', '풍강':'093380', '흥국':'010240', '창해에탄올':'004650',
                '유엔젤':'072130', '엘비세미콘':'061970', '대신정보통신':'020180', '남선알미늄':'008350'}

park_young_sun = {'제이티':'089790', '제이씨현시스템':'033320', 'imbc':'052220'}

yoo_seung_min = {'대신정보통신':'020180', '서한':'011370', '삼일기업공사':'002290', '세우글로벌':'013000', '한국선재':'025550'}

lee_nak_yeon = {'남선알미늄':'008350', '삼부토건':'001470', '이월드':'084680', '서원':'021050', 'sdn':'099220'}

ann_cheol_soo = {'써니전자':'004770', '안랩':'053800', '다믈멀티미디어':'093640', '링네트':'042500', '오픈베이스':'049480',
                '대창솔루션':'096350', '까뮤이앤씨':'013700'}

chu_mi_ae = {'제룡전기':'033100', '제룡산업':'147830', '우리들제약':'004720', '우리들휴브레인':'118000', '모헨즈':'006920'}

oh_se_hun = {'진양산업':'003780', '진양화학':'051630', 'sci평가정보':'036120'}



# 뉴스 관련 주가 차트 띄우기
count = 0
for person in list(data['words'].value_counts()[:15].index):
    if person in ['북한', '김정은', '대북']:
        for key,value in north_korea.items():
            st.write('대북 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1
        
    elif person == '윤석열':
        for key,value in yoon_seok_yeol.items():
            st.write('윤석열 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1
        
    elif person == '황교안':
        for key,value in hwang_gyo_an.items():
            st.write('황교안 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1
        
    elif person == '이재명':
        for key,value in lee_jae_myung.items():
            st.write('이재명 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1
        
    elif person == '유시민':
        for key,value in yoo_si_min.items():
            st.write('유시민 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1
        
    elif person == '박영선':
        for key,value in park_young_sun.items():
            st.write('박영선 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1
        
    elif person == '유승민':
        for key,value in yoo_seung_min.items():
            st.write('유승민 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1
        
    elif person == '이낙연':
        for key,value in lee_nak_yeon.items():
            st.write('이낙연 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1
        
    elif person == '안철수':
        for key,value in ann_cheol_soo.items():
            st.write('안철수 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1
        
    elif person == '추미애':
        for key,value in chu_mi_ae.items():
            st.write('추미애 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1

    elif person == '오세훈':
        for key,value in oh_se_hun.items():
            st.write('오세훈 테마주 : ', key, '(',value,')')
            df = fdr.DataReader(value, '2017')
            st.line_chart(df['Close'])
            count += 1


if count == 0:
    st.write('현재 뉴스 키워드 분석으로는 유용한 테마주 리스트를 추천드릴 수 없습니다. 죄송합니다.')
