"""
날짜: 2021/08/31
이름: 김예은
내용: 파이썬 Selenium(가상브라우저) 패키지 실습
"""

from selenium import webdriver

#가상브라우저 실행
browser = webdriver.Chrome('./chromedriver.exe')

#네이버이동
browser.get('https://www.naver.com/')

#로그인 버튼 클릭
login_a = browser.find_element_by_css_selector('#account > a')
login_a.click()

#아이디,비번 입력
input_id = browser.find_element_by_css_selector('#id')
input_pw = browser.find_element_by_css_selector('#pw')

input_id.send_keys('abcd')
input_pw.send_keys('1q2w3e4')


#로그인 버튼 클릭
button_login = browser.find_element_by_css_selector('#log\.login')
button_login.click()
