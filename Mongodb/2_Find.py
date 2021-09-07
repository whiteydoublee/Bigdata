"""
날짜 : 2021/09/07
이름 : 김예은
내용 : 파이썬 MongoDB Find 실습하기
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
rs = collection.find()
for row in rs:
    print('--------------------------')
    print('%s, %s, %s, %s, %s, %s'%(row['uid'], row['name'], row['hp'], row['pos'], row['dep'], row['rdate']))

#5단계 - MongoDB종료
conn.close()
