### 최초 1회 DB 세팅하는 프로그램 ###
### dbinfo.json에서 타겟 db의 정보(db주소, user, pw)를 받아
### dateweek, greatedata 테이블을 세팅해준다.
    # dateweek: 형식으로 되어있는 출석부 상 "날짜" 어트리뷰트를 date, week, day(요일)로 매칭해주는 테이블
    # greatdata: 최종적으로 준비되는 데이터를 모아놓는 테이블로, 교육생들의 이름, 영어이름, 프로필이미지를 미리 등록

import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import random, time


with open("dbinfo.json","r") as f:
    jsondata = json.load(f)

#Mongodb 연결
client = MongoClient(jsondata["dburl"],27017)
db = client.buttLvUp

#dateweek 콜렉션 생성
def dateweekColl():
    db.dateweek.drop()
    with open("date_week.json","r") as f:
        jsondata = json.load(f)
    db.dateweek.insert_many(jsondata)

#greatdata 콜렉션 초기화
def makeGreatdata():
    db.greatdata.drop
    with open("greatdata.json","r") as f:
        jsondata = json.load(f)
    db.greatdata.insert_many(jsondata)


dateweekColl()

makeGreatdata()

time.sleep(5)

#gratedata 콜렉션의 프로필이미지 초기화(1~15 랜덤값 부여)
names_data = list(db.greatdata.find({}, {"Name": 1, "_id": 0}))
names_arr = [entry['Name'] for entry in names_data]
for name in names_arr:
    db.greatdata.update_one({"Name" : name}, {"$set": {"Img" : random.randint(1,15)}})
