from flask import Flask, render_template, jsonify, request, redirect, make_response, url_for
import jwt
from pymongo import MongoClient
import datetime
import json
import sys


app = Flask(__name__)

#secret.json을 읽어 jwt 발급을 위한 시크릿 키 획득.
#시크릿 키는 보안상 secret.json 파일에 따로 보관하며 .gitignore에 등록하여 퍼블릭 업로드 되지 않도록 관리한다.
with open("secret.json","r") as f:
    jsondata = json.load(f)
    
#jwt셋업
app.config['SECRET_KEY'] = jsondata["secret-key"]

#Mongodb 연결
client = MongoClient('localhost', 27017)
db = client.buttLvUp


#####
# 아래의 각각의 @app.route 은 RESTful API 하나에 대응됩니다.
# @app.route() 의 첫번째 인자는 API 경로,
# 생략 가능한 두번째 인자는 해당 경로에 적용 가능한 HTTP method 목록을 의미합니다.

# API #1: HTML 틀(template) 전달
#         틀 안에 데이터를 채워 넣어야 하는데 이는 아래 이어지는 /api/list 를 통해 이루어집니다.

def parse_chart_JSON_data_(data_str):
    data_list = data_str.split(',')
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    week_json = []
    for day in days:
        week_json.append({'day': day, 'height': int(data_list[days.index(day)])})
    return week_json

def load_data_from_JSON(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            chart_data_str = item['chart_data']
            item['chart_data'] = parse_chart_JSON_data_(chart_data_str)
            item['number'] = str(item['number'])
            item['image_number'] = str(item['image_number'])
        
        # "number" 값을 기준으로 데이터 정렬
        data.sort(key=lambda x: int(x['number']))
        
        return data


@app.route('/')
def home():
    jwt_token = request.cookies.get('Authorization')
    #토큰 없는 경우 로그인 페이지로
    if not jwt_token:
        print("토큰없음")
        # payload_guest = {'user_id' : 'guest', 'exp': datetime.datetime.now()}
        # guest_token = jwt.encode(payload_guest, app.config['SECRET_KEY'], algorithm='HS256')
        # goto_login = make_response(render_template('login.html'))
        # goto_login.set_cookie("Authorization", guest_token)
        # return goto_login
        return render_template('login.html')
    
    #토큰 있으면 디코딩하여 user_id, 만료기간 확인
    try:
        decoded_token = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return render_template('login.html')
    user_id = decoded_token.get('user_id')
    exptime = decoded_token.get('exp')
    exptime = datetime.datetime.fromtimestamp(exptime)
    print(exptime)
    print(datetime.datetime.now())
    print(user_id)

    #토큰이 유효기간내인지 확인해서 만료면 로그인 페이지로
    if datetime.datetime.now() > exptime:
        print("기간만료")
        return render_template('login.html')
    
    #user_id를 유저풀의 ID와 대조하여 이름 등 정보 획득, 메인으로 보낸다
    current_user = db.users.find_one({'ID' : user_id})
    if current_user == None:
        print("id 없음")
        return render_template('login.html')
    
    # name = current_user["Name"]

    ## 로그인 정보를 바탕으로 메인 페이지를 렌더링
    target_name = current_user["Name"]
    ## TODO: json 파일 경로에서
    black_box_items = load_data_from_JSON('test.json')
    target_item = None
    for item in black_box_items:
        if item['name'] == target_name:
            target_item = item
            break
    if target_item:
        name = target_item['name']
        time = target_item['total_time']
        chart_data = target_item['chart_data']
        image_number = target_item['image_number']
        chart_box2_data = target_item['chart_data']
    else:
        name = target_name
        time = "00:00:00"
        chart_data = []
        image_number = "default.png"
        chart_box2_data = []
    chart_box2_data_json = json.dumps(chart_box2_data)


    return render_template('main.html', name = name, time=time, black_box_items=black_box_items, image_number=image_number, chart_box2_data_json=chart_box2_data_json)
    

@app.route('/login', methods = ['POST'])
def login():
    #클라이언트로 받은 json 내용 중 user_id와 user_password 추출
    user_id = request.get_json()['user_id']
    user_password = request.get_json()['user_password']
    print(user_id + user_password)

    #클라이언트 db의 유저 목록에서 user_id 조회
    user = db.users.find_one({'ID': user_id})
    print(user['Password'])
    if user == None:
        return jsonify({'result': 'failure'})
    if user['ID'] == user_id and user['Password'] == user_password:
        payload = {'user_id' : user_id, 'exp': datetime.datetime.now() + datetime.timedelta(minutes=1) - datetime.timedelta(hours=9)}
        access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        print(access_token)
        response = jsonify({'result': 'success', 'access_token': access_token})
        print(response)
        return {'result': 'success', 'access_token': access_token}
    
    return jsonify({'result': 'failure'})
    

@app.route("/signup", methods=['POST'])
def handle_signup():
    # 클라이언트로부터 받은 데이터를 JSON 형태로 추출
    data = request.get_json()
    full_name = data.get('full_name')
    user_id = data.get('user_id')
    user_password = data.get('user_password')

    # 유저 정보 유효성 검사 및 DB에 저장하는 로직 구현 (예시 코드)
    # 예를 들어, user_id가 이미 존재하는지 확인
    if db.users.find_one({'ID': user_id}):
        # 이미 존재하는 user_id인 경우
        return jsonify({'result': 'failure', 'message': 'User ID already exists'}), 400

    # 비밀번호 해싱 등 보안 처리 구현 필요
    hashed_password = user_password  # hash_password는 가상의 비밀번호 해싱 함수

    # 새 사용자 정보 MongoDB에 저장
    db.users.insert_one({
        'ID': user_id,
        'Name': full_name,
        'Password': hashed_password
    })

    # 회원가입 성공 응답 반환
    return jsonify({'result': 'success', 'message': 'User registered successfully'}), 200

@app.route("/signup", methods=['GET'])
def signup_page():
    return render_template("signup.html")



if __name__ == '__main__':
    print(sys.executable)
    app.run('0.0.0.0', port=5001, debug=True)