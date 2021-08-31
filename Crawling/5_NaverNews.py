"""
날짜: 2021/08/31
이름: 김예은
내용: 파이썬 가상 브라우저 뉴스 크롤링 실습
"""

import time
from selenium  import webdriver
""""""
#가상브라우저 실행
browser = webdriver.Chrome('./chromedriver.exe')

#네이버 뉴스 이동
browser.get('https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230')

i, page = 0, 1
j =0

while True:

    #수집하는 페이지 날짜 출력
    viewday=''
    span_viewday = browser.find_element_by_css_selector('#main_content > div.pagenavi_day > span.viewday')
    viewday = span_viewday.text
    print('%s 수집시작' % viewday)

    while True:
        try:
            #뉴스목록 가져오기(find_elements_by_css_selector: ul이 2개이므로 elements 복수인 메서드 사용해줘야함)
            tags_a = browser.find_elements_by_css_selector('#main_content > div.list_body.newsflash_body > ul > li > dl > dt:not(.photo) > a')

            for index, tag in enumerate(tags_a): pass
               # print('{}\t{}\t{}'.format(index+1 ,tag.text,tag.get_attribute('href')))

            #다음페이지 클릭
            pages_a = browser.find_elements_by_css_selector('#main_content > div.paging > a')
            pages_a[i].click()
            print('%d 페이지 완료...' % page)

            i+=1
            page +=1

            if page%10 ==1:
                i=1


        except:
            print('%s 데이터 수집 끝...'% viewday)
            page = 1
            i=0
            # 이전 날로 이동
            pages_day = browser.find_elements_by_css_selector('#main_content > div.pagenavi_day > a')
            pages_day[j].click()

            if j<2 :
                j+=1

            break


#브라우저 종료
browser.quit()


