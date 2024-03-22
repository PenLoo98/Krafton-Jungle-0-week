### StudyTime.json 파일을 불러와서
### DB의 studylog 콜렉션에 덤프한 뒤
### studylog 정보를 가공해 greatedata 콜렉션을 갱신하는 프로그램이다.

#### 매일 Studytime.json이 실행된 이후 한번 실행되게 설정해줄것 ####

import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import time

with open("secret.json","r") as f:
    jsondata = json.load(f)

#Mongodb 연결
client = MongoClient(jsondata["dburl"],27017)
db = client.buttLvUp

#StudyTime.json을 몽고db의 studylog 콜렉션에 덤프(매일 지우고 다시 쓴다.)
def logDump():
    db.studylog.drop()
    with open("./getFromSheet/StudyTimeJSON/StudyTime.json","r") as f:
        jsondata = json.load(f)
    db.studylog.insert_many(jsondata)

#greatdata에서 교육생 명단 만들기
names_data = list(db.greatdata.find({}, {"Name": 1, "_id": 0}))
names_arr = [entry['Name'] for entry in names_data]

#today정보로 이번주 주차 및 이번주 월~토의 날짜값 어레이 생성
#today = datetime.today().strftime("%Y-%m-%d")
todayf = datetime.utcnow() + timedelta(hours=9)
today = todayf.strftime("%Y-%m-%d")
thisweek = db.dateweek.find_one({"Date" : today})["Week"]
montosat_list = list(db.dateweek.find({"Week": thisweek, "Day": {"$ne": 0}}, {"날짜": 1, "_id": 0}).sort("Day"))
dates_arr = [entry['날짜'] for entry in montosat_list]

#직전 7일 날짜값 어레이 생성

week2tue = datetime.strptime("2024-03-26", "%Y-%m-%d")
daysdiff = (week2tue - datetime.today()).days

avgmo = 7
if daysdiff > 0:
    avgmo = 7 - daysdiff

sevendates_list = list(db.dateweek.find({"Date": {"$lt": today}}).sort("Date").limit(avgmo))
sevendates_arr = [entry['날짜'] for entry in sevendates_list]



#총시간 구하기
#일별 시간 구하는 함수
def parsetime(time_str):
    if time_str == '':
        return 0
    
    hh = 0
    mm = 0
    ss = 0
    try:
        hh, mm, ss = map(int, time_str.split(':'))
    except ValueError as e:
        hh, mm = map(int, time_str.split(':'))
        if hh<6:
            hh +=24
    delta = int(timedelta(hours=hh, minutes=mm, seconds=ss).total_seconds())
    return delta

def time_calc(dict):
    study_start_str = dict.get("학습시작시간")
    study_end_str = dict.get("학습종료시간")
    fallout_start_str = dict.get("외출시작")
    fallout_end_str = dict.get("외출종료")
    #시간형식변환
    study_start = parsetime(study_start_str)
    study_end = parsetime(study_end_str)
    fallout_start = parsetime(fallout_start_str)
    fallout_end = parsetime(fallout_end_str)

    nettime = (study_end - study_start - (fallout_end - fallout_start))/ 3600
    return nettime
   
def total_time(mylist):
    total = 0
    for dict in mylist:
        total += time_calc(dict)
    # print(total)
    return total
def total_time_format(mylist):
    total = 0
    for dict in mylist:
        total += time_calc(dict)
    hours, remainder = divmod(total, 1)
    minutes, seconds = divmod(remainder * 60, 1)
    seconds = remainder * 60
    return "{:d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

#월화수목금토
def montosat(sixdaylist):
    montosat_arr = []
    for dict in sixdaylist:
        montosat_arr.append(int(time_calc(dict)))
    
    # print(montosat_arr)
    return montosat_arr

#7일평균
def sevenavg(sevendaylist):
    seventotal = 0
    for dict in sevendaylist:
        seventotal += time_calc(dict)
    avg = seventotal / avgmo
    # print(avg)
    return avg

#greatdata 콜렉션 업데이트
def db_update():
    names_data = list(db.greatdata.find({}, {"Name": 1, "_id": 0}))
    names_arr = [entry['Name'] for entry in names_data]

    for name in names_arr:
        myname = name
        mylog = db.studylog.find({"이름": myname})
        mylist = list(mylog)
        sixdaylist = list(db.studylog.find({"이름": myname, "날짜": {"$in": dates_arr}}))
        sevendaylist = list(db.studylog.find({"이름": myname, "날짜": {"$in": sevendates_arr}}))

        tt = total_time(mylist)
        ttf = total_time_format(mylist)
        ms = montosat(sixdaylist)
        sa = sevenavg(sevendaylist)
        print(myname +" "+"업데이트")
        query = {"$set": {"Total": tt, "Mon": ms[0], "Tue": ms[1], "Wed": ms[2], "Thu": ms[3], "Fri": ms[4], "Sat": ms[5], "ttf": ttf}}
        db.greatdata.update_one({"Name": myname}, query)
    
    return

logDump()
time.sleep(5)
db_update()

