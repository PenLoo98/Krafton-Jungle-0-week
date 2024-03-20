import json
from pymongo import MongoClient

client = MongoClient('localhost',27017)
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

    # 최소값 1추가 
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

print(jsondata)
with open("test.json", "w") as json_file:
    json.dump(jsondata, json_file, indent=4, ensure_ascii= False)