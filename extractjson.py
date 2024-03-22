### DB의 greatedata 콜렉션에 저장된 데이터를
### app.py에서 다룰 수 있는 형태의 json으로 추출해주는 프로그램
### extractjson를 임포트하고 jsondata = greatjson() 으로 사용하면 됨

import json
from flask import jsonify
from pymongo import MongoClient

def greatjson():
    with open("secret.json","r") as f:
        jsondata = json.load(f)

    #Mongodb 연결
    client = MongoClient(jsondata["dburl"],27017)
    db = client.buttLvUp

    #greatdata를 json으로 추출
    greatdata = list(db.greatdata.find().sort("Total",-1))

    jsondata = []
    for entry in greatdata:
        name = entry["Name"]
        number = greatdata.index(entry) + 1
        image_number = entry["Img"]
        mon = entry["Mon"]
        tue = entry["Tue"]
        wed = entry["Wed"]
        thu = entry["Thu"]
        fri = entry["Fri"]
        sat = entry["Sat"]

        # 최소값 2추가 
        def min_set(int_num):
            if int_num <1:
                int_num =2
            return int_num
        mon = min_set(mon)
        tue = min_set(tue)
        wed = min_set(wed)
        thu = min_set(thu)
        fri = min_set(fri)
        sat = min_set(sat)

        chart_data = "{:d},{:d},{:d},{:d},{:d},{:d}".format(mon,tue,wed,thu,fri,sat)
        total_time = entry["ttf"]

        dicty = {"name": name, "number": number, "image_number": image_number, "chart_data": chart_data, "total_time": total_time}
        jsondata.append(dicty)
    
    # print(jsondata))
    # with open("test.json", "w") as json_file:
    #     json.dump(jsondata, json_file, indent=4, ensure_ascii= False)

    return jsondata