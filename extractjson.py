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
    chartdata = "{:d},{:d},{:d},{:d},{:d},{:d},".format(mon,tue,wed,thu,fri,sat)
    total_time = entry["ttf"]

    dicty = {"name": name, "number": number, "image_number": image_number, "chartdata": chartdata, "total_time": total_time}
    jsondata.append(dicty)

print(jsondata)
with open("test.json", "w") as json_file:
    json.dump(jsondata, json_file, indent=4, ensure_ascii= False)