"""
날짜: 2021/08/30
이름: 김예은
내용: 파이썬 HTML 페이지 파싱하기 실습

파싱(Parsing) - 마크업 문서(반정형)에서 특정태그의 데이터를 추출 처리하는 과정
anti-crawling -
Mozilla: Chrome브라우저의 엔진 이름
"""

import requests as req
from bs4 import BeautifulSoup as bs

#페이지 요청
url = 'https://news.naver.com/main/home.naver'
html=req.get(url, headers={'User-Agent':'Mozilla/5.0'}).text
#print(html)

#페이지 파싱
dom = bs(html, 'html.parser')
titles = dom.select('#section_it > div.com_list > div > ul > li > a > strong')
#print(titles)

#파싱데이터 출력 : *.text/string: 내용만 출력
for title in titles:
    print(title.text)

#다음 랭킹뉴스 (1~5위까지)
url='https://news.daum.net/ranking/popular'
html_daum = req.get(url).text

dom_daum = bs(html_daum, 'html.parser')
rankings = dom_daum.select('#mArticle > div.rank_news > ul.list_news2 > li> div.cont_thumb > strong > a')

for i in range(5):
    print('%d위: %s'% (i+1, rankings[i].text))
