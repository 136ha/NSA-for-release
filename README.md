# Project-NLP_Stock_Adviser  

## 1. Introduction
### 1.1. Purpose
 Recently we are living in a wave of data. The vast amount of data gives insights into our lives in many ways, and research on analyzing data is endlessly coming out. Forecasting stocks has been the goal for many people, by using statistical theory. This project aims to help various investors to invest in stocks by reading a vast amount of news coming out every minute, visualizing the amount of words related to political theme stocks, and implementing them on the web.  

### 1.2. Intended Audience
 The intended audience is not only relative to the stock, but also students who are studying for relative fields. It is mainly for users aged 18-50, but older audiences also could be the target users.

### 1.3. Intended Use
 In order to learn politics, we have to invest a lot of time to access and collect news of various leanings; conservative or progressive. However, by analyzing a large amount of news data in real time and extracting important keywords, we can save time and have a holistic view, which will give macroscopic insights to users about the everchanging society.
 
## 2. Overall Description

### 2.1. BACKEND

1. Collect breaking news data within 6 hours from the following websites;
> Google  
> Naver  
> Daum  
2. The following text pre-processing is performed;
> Remove duplicate news  
> Extract nouns  
> Remove words that are less relevant to the topic  
4. Proceed with the following visualization;  
> word cloud example:  
> ![business_anlytics_worldcloud](https://user-images.githubusercontent.com/63996621/110237364-0700d000-7f7f-11eb-9238-631d35950f21.png)  
> value count example:  
> ![business_anlytics_bar](https://user-images.githubusercontent.com/63996621/110587542-2bdf8800-81b7-11eb-99a8-8a6180df5ff0.png)  
> Interestingly, when you look at each word, it doesn't seem to have no correlation, but if you look carefully, you can see that about half of the words in the top 12 were related to the LH speculation which was hot at the time.  
5. Github workflow will be used for auto data crawling and updating database every 20 minutes. I decided to seperate crawling and frontend so that loading could be much shorter, which extremely enhanced usability.  

### 2.2. FRONTEND

In this project, streamlit, library that turns data scripts into shareable web apps in minutes, is used so that no front-end experience required.  

## 3. Requirements

### 3.1. System Required
 - jdk-15.02
 - JPype1-1.1.2-cp37-cp37m-win_amd64.whl
 - wordcloud‑1.8.1‑cp37‑cp37m‑win_amd64.whl
 - github action

### 3.2. Library Required
 - beautifulsoup4 4.9.3
 - selenium 3.141.0
 - requests 2.25.1
 - numpy 1.20.1
 - pandas 1.2.3
 - streamlit 0.78.0
 - konlpy 0.5.2
 - finance-datareader 0.9.13

## 4. Results
[prototype](https://share.streamlit.io/136ha/nsa-for-release/main/browser.py)  

## 5. References

### 5.1. Paper
 Jong Woo Kim., et al. "Influence analysis of Internet buzz to corporate performance: Individual stock price prediction using sentiment analysis of online news." J Intell Inform Syst 2015 December: 21(4): 37-51  
 Ahn Sung-Woo., et al. "Stock Prediction Using News Text Mining and Time Series Analysis." Korean Institute of Information Scientists and Engineers, 2010.06.30  

### 5.2. Blog
[Python Streamlit 사용법 - 프로토타입 만들기](https://zzsza.github.io/mlops/2021/02/07/python-streamlit-dashboard/)  
[[KR] Streamlit 웹 어플리케이션 배포하기 (feat. Heroku)](https://wonyoungseo.medium.com/kr-streamlit-%EC%9B%B9-%EC%96%B4%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0-feat-heroku-40619e933d5a)  
[How can I use konlpy with streamlit-sharing?](https://discuss.streamlit.io/t/how-can-i-use-konlpy-with-streamlit-sharing/11243)  
[[GitHub] GitHub Action을 사용하여 자동 크롤링과 Push 구현하기](https://chanhuiseok.github.io/posts/git-1/)  
[Push issue](https://github.com/ad-m/github-push-action/issues/44)  

## 6. Produced by

Yoo Jaehyeon  
email : allan3129@gmail.com  
github : https://github.com/allan02

Yoon Kiseok  
email : requests.selenium@gmail.com  
github : https://github.com/136ha
