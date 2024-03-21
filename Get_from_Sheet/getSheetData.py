import gspread
import json
import time
from itertools import chain

# json인증서, 스프레드시트 url, 파일 경로를 읽기
private_json = json.load(open('privateData.json', 'r'))

# 구글 클라우드 비밀키 JSON 파일을 불러올 경로 
load_JSON_path = private_json['load_JSON_path']
# 스프레드시트 URL
spreadsheet_url = private_json['spreadsheet_url']
# 추출한 데이터를 저장할 JSON을 저장할 경로
save_JSON_path = private_json['save_JSON_path']

gc = gspread.service_account(load_JSON_path)
doc = gc.open_by_url(spreadsheet_url)

# 오늘 날짜 구하고 맞는 인덱스 찾기 
from datetime import datetime
today = datetime.today().strftime("%Y-%m-%d")
# print(today)

# 모든 시트 이름 리스트로 가져오기 = 참가자 이름 리스트
def get_sheet_titles(doc):
    sheet_titles = doc.worksheets()
    parsed_sheet_title_list = []
    for title in sheet_titles:
        parsed_sheet_title_list.append(title.title)
    parsed_sheet_title_list.remove('안내문')
    return parsed_sheet_title_list

sheet_titles = get_sheet_titles(doc)

# 시트 이름에 맞는 데이터 가져오기 
# TODO: 불러오기 못했을 경우의 예외처리 추가하기
def save_sheet_data(doc, sheet_titles, file_path):
    for title in sheet_titles:
        jsonData = doc.worksheet(title).get_all_records()

        # TODO: JSON에 '이름' 속성 추가하기
        for data in jsonData:
            data['이름'] = title
    
        with open(file_path + title + ".json", 'w', encoding='utf-8') as file:
            json.dump(jsonData, file, ensure_ascii=False, indent=4)
        print(title + " JSON 저장 완료")
        time.sleep(2)
    return 0

save_sheet_data(doc, sheet_titles, save_JSON_path)

# JSON을 읽어 하나의 JSON으로 합치기
def merge_json(file_path, sheet_titles):
    json_list = []
    for title in sheet_titles:
        # JSON 파일 읽기
        with open(file_path + title + ".json", 'r', encoding='utf-8') as file:
            jsonData = json.load(file)
            json_list.append(jsonData)
    json_list = list(chain.from_iterable(json_list))

    # JSON 파일로 저장
    with open(file_path + "Study Time.json", 'w', encoding='utf-8') as file:
        json.dump(json_list, file, ensure_ascii=False, indent=4)
    print("통합 JSON 저장 완료")
    return json_list

merge_json(save_JSON_path, sheet_titles)