# privateData_local의 경로 불러오기 
private_json = json.load(open('privateData_local.json', 'r'))
load_JSON_path = private_json['load_JSON_path']

# 추출한 데이터 JSON 파일을 불러오기
def load_sheet_data(file_path):
    json_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        jsonData = json.load(file)
        json_list.append(jsonData)

# MongoDB에 데이터 저장하기
        
# 새벽 6시에 해당 데이터 추출과 저장하는 코드 실행하기
