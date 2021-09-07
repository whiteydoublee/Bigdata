"""
날짜 : 2021/09/07
이름 : 김예은
내용 : 파이썬 MongoDB Insert 실습하기
"""

from pymongo import MongoClient as mongo
from datetime import datetime

#1단계 - mongodb 접속
conn = mongo('mongodb://yeeunkim0701:1234@192.168.56.102:27017')

#2단계 - DB선택
db=conn.get_database('yeeunkim0701')

#3단계-Collection선택
collection = db.get_collection('Member')

#4단계-Query실행
collection.insert_one({'uid':'a101',
                       'name':'김유신',
                       'hp':'010-1234-1001',
                       'pos':'사원',
                       'dep':'101',
                       'rdate':datetime.now()})

collection.insert_one({'uid':'a102','name':'김유신','hp':'010-1234-1002'})

#5단계 - MongoDB종료
conn.close()

print('Insert 완료...')