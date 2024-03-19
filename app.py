from flask import Flask, render_template, jsonify, request, redirect, make_response
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

@app.route('/')
def home():
    jwt_token = request.cookies.get('Authorization')
    if not jwt_token:
        print("토큰없음")
        return render_template('login.html')
    decoded_token = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user_id = decoded_token.get('user_id')
    exptime = decoded_token.get('exp')
    exptime = datetime.datetime.fromtimestamp(exptime)
    print(exptime)
    print(datetime.datetime.now())
    print(user_id)
    if datetime.datetime.now() > exptime:
        print("기간만료")
        return render_template('login.html')
    current_user = db.users.find_one({'ID' : user_id})
#    if current_user == None:
 #       return render_template('main.html', name = name)
    name = current_user["Name"]
    return render_template('main.html', name = name)
    
"""
@app.route('/login', methods = ['GET'])
def loginpage():
    return render_template('login.html')
"""
@app.route('/login', methods = ['POST'])
def login():
    #클라이언트로 받은 json 내용 중 id와 password 추출
    user_id = request.get_json()['user_id']
    user_password = request.get_json()['user_password']
    print(user_id + user_password)

    #클라이언트 db의 유저 목록에서 Client_id 조회
    users = db.users
    user = db.users.find_one({'ID': user_id})
    print(user['Password'])
    if user == None:
        return jsonify({'result': 'failure'})
    if user['ID'] == user_id and user['Password'] == user_password:
        payload = {'user_id' : user_id, 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}
        access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'result': 'success', 'access_token': access_token })
    else:
        return jsonify({'result': 'failure'})

@app.route("/signup", methods = ['GET'])
def signup():
    return render_template('signup.html')



if __name__ == '__main__':
    print(sys.executable)
    app.run('0.0.0.0', port=5000, debug=True)