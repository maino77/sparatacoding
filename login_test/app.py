from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)

import hashlib, jwt, datetime

m = hashlib.sha256()
m.update('Life is too short'.encode('utf-8'))

m.update(', you need python.'.encode('utf-8'))

from pymongo import MongoClient
# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML을 주는 부분
@app.route('/index.html')
def index():
   return render_template('index.html')

@app.route('/login.html')
def login():
   return render_template('login.html')

@app.route('/login_success.html')
def login_success():
   token_receive = request.cookies.get('mytoken')
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      user_info = db.user.find_one({"id": payload['id']})
      return render_template('login_success.html', nickname=user_info["nick"])
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
   id_receive = request.form['id_give']
   pw_receive = request.form['pw_give']
   nickname_receive = request.form['nickname_give']

   pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

   db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

   return jsonify({'result': 'success', 'msg': '회원가입에 성공하였습니다!'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
SECRET_KEY = 'SPARTA'
@app.route('/api/login', methods=['POST'])
def api_login():
   id_receive = request.form['id_give']
   pw_receive = request.form['pw_give']

   # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
   pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

   # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
   result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

   # 찾으면 JWT 토큰을 만들어 발급합니다.
   if result is not None:
      # JWT 토큰에는, payload와 시크릿키가 필요합니다.
      # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
      # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
      # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
      payload = {
      'id': id_receive,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5) #언제까지 유효한지
      }

      #jwt를 암호화
      # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

      # token을 줍니다.
      return jsonify({'result': 'success', 'token': token})
   # 찾지 못하면
   else:
      return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)