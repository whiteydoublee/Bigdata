"""
날짜: 2021/09/01
이름: 김예은
내용: 파이썬 가상 브라우저 영화 리뷰 크롤링 실습
"""

from selenium import webdriver
from datetime import datetime
import logging, time

#로거 생성
logger = logging.getLogger('movie_review_logger')
logger.setLevel(logging.INFO) #로거의 제일 낮은 단계

#로그 포맷
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

#로그 핸들러
fileHandler = logging.FileHandler('./movie_review.log')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

#가상브라우저 실행
browser = webdriver.Chrome('./chromedriver.exe')
logger.info('가상브라우저 실행...')


rank = 0
while True:
    #네이버 영화 이동
    browser.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt')

    #1위 영화 클릭
    titles = browser.find_elements_by_css_selector('#old_content > table > tbody > tr > td.title > div > a')
    titles[rank].click()
    # print(len(titles))

    #평점 클릭
    tabScore = browser.find_element_by_css_selector('#movieEndTabMenu > li:nth-child(5) > a')
    tabScore.click()

    #영화제목
    movie_title = browser.find_element_by_css_selector('#content > div.article > div.wide_info_area > div.mv_info > h3 > a')
    print('%s 리뷰 수집 시작' % movie_title)
    logger.info('%s 리뷰 수집시작' % movie_title)

    #현재 가상 브라우저의 제어를 영화 리뷰 iframe으로 전환
    browser.switch_to.frame('pointAfterListIframe')

    current_page=1
    while True:

        #영화 리뷰 출력
        #reviews= browser.find_element_by_css_selector('body > div > div > div.score_result > ul > li')
        #span 이 관람객표시가 된 경우, span2 관람객 표시가 없는 경우, span이 첫 번째가 되므로, last-child를 해줌
        lis = browser.find_elements_by_css_selector('div.score_result > ul > li')
        #span_review[0].click()

        for li in lis:
            try:
                li.find_element_by_css_selector('.score_reple > p a').click()

            except Exception as e:
                pass

            finally:
                score = li.find_element_by_css_selector('div.star_score > em').text
                reple = li.find_element_by_css_selector('div.score_reple > p > span:last-child').text
                #print('{},{}'.format(score,reple))

        try:
            #다음 페이지 이동
            pg_next = browser.find_element_by_css_selector('div.paging > div > a.pg_next')
           # current_page= browser.find_element_by_css_selector('div.paging > div > a > span.on')
            pg_next.click()

            print('%d 페이지완료...'%current_page)
            logger.info('%d 페이지완료...'%current_page)
            current_page+=1
        except:
            break
    """
    except Exception as e:
        print()
    finally:
    """
    print('%s 영화 리뷰 수집 완료...' % movie_title)
    logger.info('%s 영화 리뷰 수집 완료...' % movie_title)
    rank += 1

    if rank >= 50:
        rank = 0

        try:
            #영화 랭킹 페이지에서 다음 버튼 클릭
            next = browser.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a')
            next.click()
        except:
            break
print('영화 랭키 리뷰 데이터 수집 최종완료...')