"""
날짜: 2021/09/07
이름: 김예은
내용: 파이썬 가상 브라우저 영화 리뷰 크롤링 MongoDB 실습
"""

from selenium import webdriver
from datetime import datetime
import logging, time
from pymongo import MongoClient as mongo

# 로거생성
logger = logging.getLogger('movie_review_logger')
logger.setLevel(logging.INFO)

# 로그 포맷 설정
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 로그 핸들러
fileHandler = logging.FileHandler('./MovieReview.log')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

# 가상 브라우저 실행(Headless 모드로 실행)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# 보통의 FHD화면을 가정
chrome_options.add_argument('window-size=1920x1080')
# gpu를 사용하지 않도록 설정
chrome_options.add_argument("disable-gpu")
# headless탐지 방지를 위해 UA를 임의로 설정
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)")

browser = webdriver.Chrome('./chromedriver.exe', options=chrome_options)
logger.info('가상 브라우저 실행...')

# MongoDB 접속
conn = mongo('mongodb://yeeunkim0701:1234@192.168.56.102:27017')
db = conn.get_database('yeeunkim0701')
collection = db.get_collection('MovieReview')

rank = 0

while True:
    # 네이버 영화 이동
    browser.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt')

    # 랭킹 영화 클릭
    titles = browser.find_elements_by_css_selector('#old_content > table > tbody > tr > td.title > div > a')
    titles[rank].click()

    #print(len(titles))
    # 평점 클릭
    tab_score = browser.find_element_by_css_selector('#movieEndTabMenu > li:nth-child(5) > a')
    tab_score.click()

    # 영화 제목
    movie_title = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
    print('%s 리뷰 수집 시작...' % movie_title)
    logger.info('%s 리뷰 수집 시작...'% movie_title)

    # 현재 가상 브라우저의 제어를 영화 리뷰 iframe으로 전환
    browser.switch_to.frame('pointAfterListIframe')

    current_page = 1
    while True:
        #영화 리뷰 출력
        lis = browser.find_elements_by_css_selector('div.score_result > ul > li')
        for li in lis:
            try:
                li.find_element_by_css_selector('.score_reple > p a').click()
            except Exception as e:
                pass
            finally :
                score = li.find_element_by_css_selector('.star_score > em').text
                reple = li.find_element_by_css_selector('.score_reple > p > span:last-child').text

                collection.insert_one({'title': movie_title,
                                       'score': score,
                                       'reple': reple})

        try:
            #다음페이지 이동
            pg_next = browser.find_element_by_css_selector('div.paging > div > a.pg_next')
            pg_next.click()

            print('%d 페이지 완료...' % current_page)
            logger.info('%d 페이지 완료...' % current_page)

            current_page += 1

        except:
            break


    #print('%s 영화 리뷰 수집완료...' % movie_title)
    logger.info('%s 영화 리뷰 수집완료...' % movie_title)

    rank += 1

    if rank == 50:
        rank = 0
        try:
            # 영화 랭킹 페이지에서 다음 버튼 클릭
            next = browser.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a')
            next.click()
        except:
            break


#print('영화랭킹 리뷰 데이터 수집 최종완료...')
logger.info('영화랭킹 리뷰 데이터 수집 최종완료...')

# MongoDB 종료
conn.close()

# 브라우저 종료
browser.quit()